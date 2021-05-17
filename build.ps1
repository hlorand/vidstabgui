
# Install Pyinstaller
pip3 install pyinstaller

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

# Build Using Pyinstaller
pyinstaller.exe --onefile -w "vidstabgui.py"

# Remove unnecessary folders
Remove-Item __pycache__ -Recurse
Remove-Item build -Recurse
Remove-Item vidstabgui.spec
Remove-Item vidstabgui.exe
Move-Item dist\vidstabgui.exe .
Remove-Item dist -Recurse

# Create zip file
$date = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path .\*.exe -DestinationPath "vidstabgui-win-$date.zip"

explorer .