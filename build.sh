
# Install Pyinstaller
pip3 install pyinstaller

# Download ffmpeg
rm ffmpeg-4.4.zip ffmpeg
wget https://evermeet.cx/ffmpeg/ffmpeg-4.4.zip
unzip ffmpeg-4.4.zip
rm ffmpeg-4.4.zip

# Build Using Pyinstaller
pyinstaller --onefile -w "vidstabgui.py"

# Remove unnecessary folders
rm -rf __pycache__
rm -rf build
rm vidstabgui.spec
mv dist/vidstabgui.app .
rm -rf dist

# Create zip file
date=$(date +"%Y-%m-%d")
zip -r "vidstabgui-osx-"$date".zip" ./vidstabgui.app ffmpeg

open .