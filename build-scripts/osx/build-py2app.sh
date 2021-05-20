#!/bin/bash

cd ../../

# Install Pyinstaller
sudo pip3 install py2app
sudo pip3 install --upgrade py2app

# Download ffmpeg
rm ffmpeg-4.4.zip ffmpeg
wget https://evermeet.cx/ffmpeg/ffmpeg-4.4.zip
unzip ffmpeg-4.4.zip
rm ffmpeg-4.4.zip

# Build Using Pyinstaller
rm setup.py
py2applet --make-setup vidstabgui.py ffmpeg icon/icon.icns
python3 setup.py py2app

# Remove unnecessary files and folders
rm ffmpeg
rm -rf build
rm setup.py
rm -rf vidstabgui.app
mv dist/vidstabgui.app .
rm -rf dist

# Create zip file
date=$(date +"%Y-%m-%d")
rm "vidstabgui-osx-"$date".zip"
zip -r "vidstabgui-osx-"$date".zip" ./vidstabgui.app

open .