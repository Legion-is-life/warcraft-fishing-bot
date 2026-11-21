import queue
import unittest
from unittest.mock import Mock, patch
import sys

# Exercise the real worker on machines without a Windows audio device.
with patch.dict(sys.modules, {name: Mock() for name in
                              ("win32api", "win32gui", "win32con", "pyaudiowpatch")}):
    import app

app.win32con.VK_F1 = 112
app.win32con.VK_F6 = 117


class FishingTests(unittest.TestCase):
    def worker(self, **kwargs):
        return app.Worker(queue.Queue(), {"threshold": -45}, 1, app.DEFAULT_OUTPUT,
                          kwargs.get("initial", True), app.LureSettings(**kwargs.get("cfg", {})),
                          kwargs.get("last"))

    def test_worker_cycle(self):
        for enabled, initial, expected in (
            (True, True, ["F7", "F6", "listen", "read", "F6", "end", "F7", "F6"]),
            (False, True, ["F6", "listen", "read", "F6", "end", "F6"]),
            (True, False, ["listen", "read", "F6", "end", "F7", "F6"]),
        ):
            with self.subTest(enabled=enabled, initial=initial):
                w = self.worker(cfg={"enabled": enabled}, initial=initial,
                                last=None if initial else 0)
                trace = []
                clock = [0]
                stream = Mock()
                def read(*args, **kwargs):
                    clock[0] = 601
                    trace.append("read")
                    return bytes([255, 63]) * 2048
                stream.read.side_effect = read
                stream.start_stream.side_effect = lambda: trace.append("listen")
                stream.stop_stream.side_effect = lambda: trace.append("end")
                audio = Mock()
                audio.get_default_wasapi_loopback.return_value = dict(
                    name="Test speakers", index=8, isLoopbackDevice=True,
                    defaultSampleRate=48000, maxInputChannels=2)
                audio.open.return_value = stream
                def press(key):
                    trace.append(f"F{key - 111}")
                    if "end" in trace and key == 117:
                        w.stop.set()
                with patch.object(w, "press", side_effect=press), \
                     patch.object(w.stop, "wait", side_effect=lambda _: w.stop.is_set()), \
                     patch.object(app.time, "monotonic", side_effect=lambda: clock[0]), \
                     patch.object(app.pyaudio, "PyAudio", return_value=audio):
                    w.run()
                self.assertEqual(trace, expected)
                audio.open.assert_called_once_with(format=app.pyaudio.paInt16, channels=2,
                    rate=48000, input=True, input_device_index=8,
                    frames_per_buffer=app.CHUNK, start=False)
                stream.close.assert_called_once()

    def test_interval_resume_and_new_session(self):
        w = self.worker(last=10, cfg={"key": "F8", "delay": 0})
        with patch.object(w, "press") as press:
            for now, keys in ((599, [117]), (600, [119, 117]), (601, [117])):
                with patch.object(app.time, "monotonic", return_value=now):
                    self.assertTrue(w.before_cast())
                self.assertEqual([c.args[0] for c in press.call_args_list], keys)
                press.reset_mock()
        self.assertIsNone(self.worker().last_attempt)

    def test_stop_during_application_and_before_cast(self):
        w = self.worker()
        with patch.object(w, "press") as press:
            def stop(delay):
                self.assertGreater(delay, 0)
                w.stop.set()
                return True
            with patch.object(w.stop, "wait", side_effect=stop):
                self.assertFalse(w.before_cast())
                self.assertFalse(w.before_cast())
            press.assert_called_once_with(118)

    def test_failed_attempt_is_remembered(self):
        w = self.worker()
        with patch.object(w, "press", side_effect=OSError), self.assertRaises(OSError):
            w.before_cast()
        self.assertIsNotNone(w.last_attempt)

    def test_key_pair(self):
        w = self.worker()
        app.win32api.MapVirtualKey.return_value = 42
        with patch.object(app.win32api, "PostMessage") as post:
            w.press(118)
            self.assertEqual([c.args[1:3] for c in post.call_args_list],
                             [(app.win32con.WM_KEYDOWN, 118), (app.win32con.WM_KEYUP, 118)])

    def test_invalid_settings(self):
        for fields in ({"key": "F6"}, {"key": ""}, {"interval": 0}, {"delay": float("nan")}):
            with self.assertRaises(ValueError):
                app.LureSettings(**fields)
