# this PowerShell script prepares certain other files for use with PyInstaller and Inno Setup

# create a doc directory and all required subdirs
New-Item -ItemType Directory 'doc\'
$folders = @("CustomTkinter", "CTkListbox", "Plyer", "Pyperclip", "DarkDetect")
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path "doc\$folder" -Force
}

# get the license files from GitHub
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt" -OutFile "doc\MIT.txt"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/spdx/license-list-data/main/text/BSD-3-Clause.txt" -OutFile "doc\BSD-3-Clause.txt"

# copy the licenses to their appropriate places, moving them on the last one to avoid leftover mess
Copy-Item -Path "doc\MIT.txt" -Destination "doc\CustomTkinter\LICENSE"
Copy-Item -Path "doc\MIT.txt" -Destination "doc\CTkListbox\LICENSE"
Move-Item -Path "doc\MIT.txt" -Destination "doc\Plyer\LICENSE"
Copy-Item -Path "doc\BSD-3-Clause.txt" -Destination "doc\Pyperclip\LICENSE"
Move-Item -Path "doc\BSD-3-Clause.txt" -Destination "doc\DarkDetect\LICENSE"

python convert-to-ico.py # convert the PNG file to ICO format
python -m PyInstaller JSONly.spec # compile the Python files to EXE with PyInstaller
