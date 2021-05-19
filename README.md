# VidStab GUI

A simple graphical user interface for the [VidStab](https://github.com/georgmartius/vid.stab) video stabilization library.

You can download the application to Windows or OSX at the [releases page](https://github.com/hlorand/vidstabgui/releases)

![](https://raw.githubusercontent.com/hlorand/vidstabgui/assets/screenshot.gif)

## Build

**Windows**

Requirements:

- [py2exe](https://pypi.org/project/py2exe/)

- Open an administrative Power Shell
- Run `.\build-scripts\win\build-py2exe.ps1`
	- The configuration file for the script is `build-scripts\win\setup.py`

**OSX**

Requirements:

- [pyinstaller](https://pypi.org/project/pyinstaller/)

- Open a Terminal
- `chmod +x ./build-scripts/osx/build-pyinstaller.sh`
- Run `./build-scripts/osx/build-pyinstaller.sh`