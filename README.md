# 1st World of Warcraft Audio-based Fishing Bot

**1st World of Warcraft Audio-based Fishing Bot** programmed in Python. It uses the audio output of World of Warcraft window to automatically fish.

![Image](https://static.icy-veins.com/images/wow/og-image-fishing.jpg)

## Compatibility

Works only on retail (World of Warcraft Dragonflight).

#### Supported Platforms

| Platform | Status                     |
|:--------:|:--------------------------:|
| Windows  | :green_heart: Supported    |
| MacOS    | :grey_question: Not tested |
| Linux    | :grey_question: Not tested |

## Getting Started

1. For WASAPI loopback capture, run the Python version using the installation steps below. The bundled executable still uses Stereo Mix.

2. Select the playback device used by World of Warcraft, or leave Windows default selected. Use **Refresh devices** after connecting a headset. Check the dB meter when game sound plays.

3. Install addon called [Better Fishing](https://www.curseforge.com/wow/addons/better-fishing).

4. Make sure that the addon's keybind ```Cast and Interact``` is bind to F6.

5. Turn off every sound type except ```Sound Effects```. And set your sound volume to following:
    - Master Volume (5% is recommended at 100% system volume, but this can vary based on your system settings.)
    - Music 0%
    - Effects 100%
    - Ambience 0%
    - Dialog 0%

6. Go to a silent place and run the ```app.exe``` or ```app.py``` and let the bot do the work. It is recommended to not do anything else on the computer while the bot is fishing, because you can interfere with the sound output!

#### Python script

1. You need to install [Python](https://www.python.org/downloads/) onto your computer.

2. After you have installed Python, you need to install all the required libraries to run the fishing bot script. Run ```pip install -r requirements.txt``` in the terminal.

## Disclaimer
Using the **1st World of Warcraft Audio-based Fishing Bot** may violate the World of Warcraft's terms of service and result in penalties, including getting banned. The creator of the **1st World of Warcraft Audio-based Fishing Bot** is not liable for any consequences or damages caused by its use. Use at your own risk!
### Automatic Shiny Baubles (Python app)

Equip your main-hand fishing pole, put this macro on an action bar, and bind it
to F7 (or choose another F1–F12 key in the app). Keep F6 bound to the fishing
addon for both casting and looting.

```text
#showtooltip Shiny Bauble
/use Shiny Bauble
/use 16
```

Automatic lures default to enabled, with a 600-second lure duration, a
590-second refresh interval and a 1.5-second delay before casting. The worker
sends the macro once before the first cast. If a refresh comes due while
listening, it waits until the current fishing cycle finishes. The timer tracks
keypress attempts; the app cannot check inventory or confirm the in-game buff.

Start saves lure settings to `%APPDATA%\FishingAssistant\lures.json`.
Stop pauses the session; Start resumes listening and checks the timer before
the next cast. Reopening the app starts a fresh session.
