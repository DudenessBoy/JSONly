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

cp ../../main.pyw ./JSONly # make a copy of the program that will be executable

# add a shebang and mark it executable
sed -i '1i #!/usr/bin/python3' JSONly
chmod +x JSONly

# get the version and store it in a variable
ensureFile ../../version.txt "The file '../../version.txt' does not exist. Please create this file so that the script can write the version to certain files."
version=$(<../../version.txt)

# get additional licenses that will be used
wget -O MIT.txt https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt
wget -O BSD-3-Clause.txt https://raw.githubusercontent.com/spdx/license-list-data/main/text/BSD-3-Clause.txt
wget -O xsel-license.txt https://raw.githubusercontent.com/kfish/xsel/refs/heads/master/COPYING

# set up the .deb setup directory

# create necessary directories
createDir deb/DEBIAN
createDir deb/usr/bin
createDir deb/usr/share/JSONly/lib
createDir deb/usr/share/applications
createDir deb/usr/share/doc/customtkinter
createDir deb/usr/share/doc/darkdetect
createDir deb/usr/share/doc/JSONly
createDir deb/usr/share/doc/CTkListbox
createDir deb/usr/local/share/icons/hicolor/64x64/apps/

declare -a control=(
    "Package: jsonly"
    "Version: $version"
    "Section: editors"
    "Architecture: amd64"
    "Maintainer: Luke Moyer <DudenessBoy-software@proton.me>"
    "Depends: xsel, python3 (>= 3.10), python3-plyer, python3-tk, python3-packaging"
    "Description: A GUI JSON editor"
    " JSONly is a GUI program for interacting with and manipulating JSON files"
)

# Write each line to the control file
for line in "${control[@]}"; do
    echo "$line" >> deb/DEBIAN/control
done

# copy the other application elements into the folder
cp ../JSONly.desktop deb/usr/share/applications/
cp ../../LICENSE deb/usr/share/doc/JSONly/
cp ../../icon.png deb/usr/local/share/icons/hicolor/64x64/apps/JSONly.png
cp -r ../../JSONly/ deb/usr/share/JSONly/lib/
cp JSONly deb/usr/bin/
ensureFolder /usr/lib/python3/dist-packages/customtkinter/ "CustomTkinter is not installed on your computer. Please install it with 'sudo pip3 install customtkinter'"
cp -r /usr/lib/python3/dist-packages/customtkinter/ deb/usr/share/JSONly/lib/
ensureFolder /usr/local/lib/python3.11/dist-packages/darkdetect "DarkDetect is not installed on your computer. Please install it with 'sudo pip3 install darkdetect'"
cp -r /usr/local/lib/python3.11/dist-packages/darkdetect deb/usr/share/JSONly/lib/
ensureFolder /usr/local/lib/python3.11/dist-packages/CTkListbox "CTkListbox is not installed on your computer. Please install it with 'sudo pip3 install CTkListbox'"
cp -r /usr/local/lib/python3.11/dist-packages/CTkListbox deb/usr/share/JSONly/lib/
declare -a mit=(
    customtkinter
    CTkListbox
    plyer
)
for i in "${mit[@]}"; do
    if [[ $i != "plyer" ]]; then
        cp MIT.txt "deb/usr/share/doc/$i/LICENSE"
    fi
done
cp ../../LICENSE deb/usr/share/doc/JSONly/
cp ../../PSFL.txt deb/usr/share/doc/JSONly/

# set up the AppImage setup directory

# create necessary directories
createDir appimage/usr/bin/
createDir appimage/usr/lib/python3.11
createDir appimage/usr/lib/python3/dist-packages/
createDir appimage/usr/share/doc/customtkinter/
createDir appimage/usr/share/doc/darkdetect/
createDir appimage/usr/share/doc/JSONly/
createDir appimage/usr/share/doc/CTkListbox
createDir appimage/usr/share/doc/Python
createDir appimage/usr/share/doc/plyer
createDir appimage/usr/share/doc/xsel

# copy application elements
cp JSONly appimage/usr/bin/JSONly
cp -r ../../JSONly/ appimage/usr/lib/python3/dist-packages/
cp ../JSONly.desktop appimage/app.desktop
cp ../../icon.png appimage/app.png
cp ../AppRun appimage/
ensureFile /usr/bin/python3.11 "Python 3.11 is not installed on your computer. Please install it with 'sudo apt install python3.11' or your distro's equivalent."
cp /usr/bin/python3.11 appimage/usr/bin/
ensureFile /usr/bin/xsel "xsel is not installed on your computer. Please install it with 'sudo apt install xsel' or your distro's equivalent."
cp /usr/bin/xsel appimage/usr/bin
# don't need to make sure they exist, this was done earlier
cp -r /usr/lib/python3/dist-packages/customtkinter/ appimage/usr/lib/python3/dist-packages/
cp -r /usr/local/lib/python3.11/dist-packages/darkdetect appimage/usr/lib/python3/dist-packages/
cp -r /usr/local/lib/python3.11/dist-packages/CTkListbox appimage/usr/lib/python3/dist-packages/
# these ones we still do since they can just be dependencies of the .deb package but need to be bundled with the AppImage
ensureFolder /usr/local/lib/python3.11/dist-packages/plyer "Plyer is not installed on your computer. Please install it with 'sudo pip3 install plyer'"
cp -r /usr/lib/python3/dist-packages/plyer/ appimage/usr/lib/python3/dist-packages/
ensureFolder /usr/local/lib/python3.11/dist-packages/plyer "Python Packaging is not installed on your computer. Please install it with 'sudo pip3 install packaging'"
cp -r /usr/lib/python3/dist-packages/packaging/ appimage/usr/lib/python3/dist-packages/
pypath=/usr/lib/python3.11
message="Your Python install is broken. Please reinstall."
ensureFolder $pypath/tkinter "Tkinter is not installed on your computer. Please install it with 'sudo apt install python3-tk' or your distro's equivalent."
cp -r $pypath/tkinter appimage/usr/lib/python3.11
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
    cp MIT.txt "appimage/usr/share/doc/$i/LICENSE"
done
cp BSD-3-Clause.txt "appimage/usr/share/doc/darkdetect/LICENSE"
cp xsel-license.txt "appimage/usr/share/doc/xsel/LICENSE"
cp ../../LICENSE "appimage/usr/share/doc/JSONly/"
cp ../../PSFL.txt "appimage/usr/share/doc/JSONly/"
cp ../../PSFL.txt "appimage/usr/share/doc/Python/LICENSE"

# change the icon line in app.desktop to use "app" instead of "JSONly"
sed -i "5s/.*/Icon=app/" appimage/app.desktop
