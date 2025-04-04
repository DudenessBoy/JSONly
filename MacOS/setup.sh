#!/bin/sh

# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# create directories
mkdir -p JSONly/resources/doc/
mkdir -p JSONly/JSONly

# get the license files from the internet
wget -O JSONly/resources/doc/MIT.txt https://raw.githubusercontent.com/spdx/license-list-data/main/text/MIT.txt
wget -O JSONly/resources/doc/BSD-3-Clause.txt https://raw.githubusercontent.com/spdx/license-list-data/main/text/BSD-3-Clause.txt

# copy the source files over
cp ../main.pyw JSONly/
cp -r ../JSONly/* JSONly/JSONly/

# convert the PNG icon to ICNS format using the Python script
python3.13 convert-to-icns.py

# create the .app bundle
cd JSONly
python3.13 setup.py py2app

# create the DMG installer file
mkdir -p dist/dmg-staging
cp -R dist/JSONly.app dist/dmg-staging/
ln -s /Applications dist/dmg-staging
hdiutil create -size 100m -fs HFS+ -volname "JSONly" -srcfolder dist/dmg-staging dist/JSONly.dmg
# finalize the DMG
hdiutil convert dist/JSONly.dmg -format UDZO -o dist/JSONly-final.dmg

# clean up temporary files
rm dist/dmg-staging/JSONly.app
rm dist/JSONly.dmg
mv dist/JSONly-final.dmg dist/JSONly.dmg
