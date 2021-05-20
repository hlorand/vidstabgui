# VidStab GUI

A simple graphical user interface for the [VidStab](https://github.com/georgmartius/vid.stab) video stabilization library.

You can download the application to Windows or OSX at the [releases page](https://github.com/hlorand/vidstabgui/releases)

![](https://raw.githubusercontent.com/hlorand/vidstabgui/assets/screenshot.gif)

## Build

**Windows (64 bit)**

- Requirements: [py2exe](https://pypi.org/project/py2exe/)
- Open an administrative Power Shell
- Navigate to `build-scripts\win\`
- Run `.\build-py2exe.ps1`
	- The configuration file for the script is: `setup.py`

For 32 bit Windows you can use this build script, the only difference is that after the script finished, you have to manually download a [32 bit ffmpeg build](https://github.com/advancedfx/ffmpeg.zeranoe.com-builds-mirror/releases/tag/20200915) and replace `dist\ffmpeg.exe` with it (which is a 64 bit build).

**OSX**

- Requirements: [py2app](https://pypi.org/project/py2app/)
- Open a Terminal
- Navigate to `build-scripts/osx/`
- `chmod +x ./build-py2app.sh`
- Run `./build-py2app.sh`
