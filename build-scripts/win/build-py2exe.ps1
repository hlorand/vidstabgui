
cd ..\..\

# Install Py2exe
pip3 install py2exe
pip3 install --upgrade py2exe

# Download ffmpeg
Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile .\ffmpeg-release-essentials.zip 
Expand-Archive .\ffmpeg-release-essentials.zip -DestinationPath .
Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/release-version -OutFile .\version.txt
$version = cat version.txt
Remove-Item ffmpeg.exe
Move-Item "ffmpeg-$version-essentials_build\bin\ffmpeg.exe" .
Remove-Item "ffmpeg-$version-essentials_build" -Recurse
Remove-Item ffmpeg-release-essentials.zip
Remove-Item version.txt

# Build Using Py2exe
python .\build-scripts\win\setup.py install
python .\build-scripts\win\setup.py py2exe

# Remove unnecessary folders
Remove-Item ffmpeg.exe

# Create zip file
$date = Get-Date -Format "yyyy-MM-dd"
Remove-Item "vidstabgui-win-$date.zip"
Compress-Archive -Path .\dist\* -DestinationPath "vidstabgui-win-$date.zip"

explorer .