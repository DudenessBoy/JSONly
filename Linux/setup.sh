#!/bin/bash

# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# this is a script that builds the folder structure for the .deb and AppImage distributions of JSONly
# DISCLAIMER: this file isn't super well written and could break without real cause on your system. It works on my computer, and that's really all I need it to do right now. I may make it better in the future.

# function to check if a directory exists, and create it if not
createDir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
    fi
}

# function that will ensure a file's existance. If the file doesn't exist, print a message and exit.
ensureFile() {
    if [[ ! -f "$1" ]]; then
        echo "$2"
        exit 1
    fi
}

# same as ensureFile, but for folders
ensureFolder() {
    if [[ ! -d "$1" ]]; then
        echo "$2"
        exit 1
    fi
}

mkdir dist/
cd dist

cp ../../main.pyw ./jsonly # make a copy of the program that will be executable

# add a shebang and mark it executable
sed -i '1i #!/usr/bin/python3' jsonly
chmod +x jsonly

# get the version and store it in a variable
ensureFile ../../version.txt "The file '../../version.txt' does not exist. Please create this file so that the script can write the version to certain files."
version=$(<../../version.txt)

# get additional licenses that will be used
wget -O BSD-3-Clause.txt https://raw.githubusercontent.com/spdx/license-list-data/main/text/BSD-3-Clause.txt
wget -O xsel-license.txt https://raw.githubusercontent.com/kfish/xsel/refs/heads/master/COPYING
wget -O PSFL.txt https://raw.githubusercontent.com/test-unit/test-unit/refs/heads/master/PSFL

# set up the .deb setup directory

# create necessary directories
createDir deb/DEBIAN
createDir deb/usr/bin
createDir deb/usr/share/JSONly/lib
createDir deb/usr/share/applications
createDir deb/usr/share/doc/customtkinter
createDir deb/usr/share/doc/darkdetect
createDir deb/usr/share/doc/CTkListbox
createDir deb/usr/local/share/icons/hicolor/64x64/apps/

declare -a control=(
    "Package: jsonly"
    "Version: $version"
    "Section: editors"
    "Architecture: amd64"
    "Maintainer: Luke Moyer <DudenessBoy-software@proton.me>"
    "Depends: xsel, python3 (>= 3.10), python3-plyer, python3-tk, python3-packaging", "python3-setuptools"
    "Description: A GUI JSON editor"
    " JSONly is a GUI program for interacting with and manipulating JSON files"
)

# Write each line to the control file
for line in "${control[@]}"; do
    echo "$line" >> deb/DEBIAN/control
done

# copy the other application elements into the folder
cp ../JSONly.desktop deb/usr/share/applications/
cp -r ../../lang/ deb/usr/share/JSONly/
cp ../../LICENSE deb/usr/share/JSONly/
cp ../../icon.png deb/usr/local/share/icons/hicolor/64x64/apps/JSONly.png
cp ../../icon.png deb/usr/share/JSONly/
cp -r ../../JSONly/ deb/usr/share/JSONly/lib/
# change the packaging variable in constants.py
sed -i "19s/.*/        packaging = 'system'/" deb/usr/share/JSONly/lib/JSONly/constants.py
cp jsonly deb/usr/bin/
ensureFolder ../../.venv/lib/python3.11/site-packages/customtkinter/ "CustomTkinter is not installed on your computer. Please install it with 'sudo pip3 install customtkinter'"
cp -r ../../.venv/lib/python3.11/site-packages/customtkinter/ deb/usr/share/JSONly/lib/
ensureFolder ../../.venv/lib/python3.11/site-packages/darkdetect "DarkDetect is not installed on your computer. Please install it with 'sudo pip3 install darkdetect'"
cp -r ../../.venv/lib/python3.11/site-packages/darkdetect deb/usr/share/JSONly/lib/
ensureFolder ../../.venv/lib/python3.11/site-packages/CTkListbox "CTkListbox is not installed on your computer. Please install it with 'sudo pip3 install CTkListbox'"
cp -r ../../.venv/lib/python3.11/site-packages/CTkListbox deb/usr/share/JSONly/lib/
declare -a mit=(
    customtkinter
    CTkListbox
    plyer
)
for i in "${mit[@]}"; do
    if [[ $i != "plyer" ]]; then
        cp ../../LICENSE "deb/usr/share/doc/$i/LICENSE"
    fi
done
cp ../../LICENSE deb/usr/share/JSONly/

# set up the AppImage setup directory

# create necessary directories
createDir appimage/usr/bin/
createDir appimage/usr/lib/python3.11
createDir appimage/usr/lib/python3/dist-packages/
createDir appimage/usr/share/doc/customtkinter/
createDir appimage/usr/share/doc/darkdetect/
createDir appimage/usr/share/doc/CTkListbox
createDir appimage/usr/share/doc/Python
createDir appimage/usr/share/doc/plyer
createDir appimage/usr/share/doc/xsel
createDir appimage/usr/share/JSONly/lang

# copy application elements
cp jsonly appimage/usr/bin/
cp ../../lang/* appimage/usr/share/JSONly/lang
cp -r ../../JSONly/ appimage/usr/lib/python3/dist-packages/
sed -i "19s/.*/        packaging = 'appimage'/" appimage/usr/lib/python3/dist-packages/JSONly/constants.py
cp ../JSONly.desktop appimage/app.desktop
cp ../../icon.png appimage/app.png
cp ../../icon.png appimage/usr/share/JSONly/
cp ../AppRun appimage/
ensureFile ../../.venv/bin/python3.11 "Python 3.11 is not installed on your computer. Please install it with 'sudo apt install python3.11' or your distro's equivalent."
cp /usr/bin/python3.11 appimage/usr/bin/
ensureFile /usr/bin/xsel "xsel is not installed on your computer. Please install it with 'sudo apt install xsel' or your distro's equivalent."
cp /usr/bin/xsel appimage/usr/bin
# don't need to make sure they exist, this was done earlier
cp -r ../../.venv/lib/python3.11/site-packages/customtkinter/ appimage/usr/lib/python3/dist-packages/
cp -r ../../.venv/lib/python3.11/site-packages/darkdetect appimage/usr/lib/python3/dist-packages/
cp -r ../../.venv/lib/python3.11/site-packages/CTkListbox appimage/usr/lib/python3/dist-packages/
# these ones we still do since they can just be dependencies of the .deb package but need to be bundled with the AppImage
ensureFolder ../../.venv/lib/python3.11/site-packages/plyer "Plyer is not installed on your computer. Please install it with 'sudo pip3 install plyer'"
cp -r ../../.venv/lib/python3.11/site-packages/plyer/ appimage/usr/lib/python3/dist-packages/
ensureFolder ../../.venv/lib/python3.11/site-packages/packaging "Python Packaging is not installed on your computer. Please install it with 'sudo pip3 install packaging'"
cp -r ../../.venv/lib/python3.11/site-packages/packaging/ appimage/usr/lib/python3/dist-packages/
pypath=../../.venv/lib/python3.11/site-packages
message="Your Python install is broken. Please reinstall."
ensureFolder /lib/python3.11/tkinter "Tkinter is not installed on your computer. Please install it with 'sudo apt install python3-tk' or your distro's equivalent."
cp -r /lib/python3.11/tkinter appimage/usr/lib/python3.11
declare -a pyapps=(
    platform.py
    subprocess.py
    webbrowser.py
)
for i in "${pyapps[@]}"; do
    ensureFile "$pypath/$i"
    cp "$pypath/$i" appimage/usr/lib/python3.11/
done
ensureFolder $pypath/json $message
cp -r $pypath/json appimage/usr/lib/python3.11

for i in "${mit[@]}"; do
    cp ../../LICENSE "appimage/usr/share/doc/$i/LICENSE"
done
cp BSD-3-Clause.txt "appimage/usr/share/doc/darkdetect/LICENSE"
cp xsel-license.txt "appimage/usr/share/doc/xsel/LICENSE"
cp ../../LICENSE "appimage/usr/share/JSONly/"
cp PSFL.txt "appimage/usr/share/doc/Python/LICENSE"

# change the icon line in app.desktop to use "app" instead of "JSONly"
sed -i "5s/.*/Icon=app/" appimage/app.desktop
# change exec to AppRun
sed -i "4s/.*/Exec=AppRun %F/" appimage/app.desktop
