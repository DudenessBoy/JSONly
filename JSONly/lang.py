# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

import json
import glob
import os
from JSONly.constants import *

keys = [ # a list of all keys that should be present in the lang file
    'menubar.file',
    'menubar.edit',
    'menubar.about',
    'menubar.settings',
    'menubar.file.open',
    'menubar.file.save',
    'menubar.file.saveas',
    'menubar.file.exit',
    'menubar.edit.add',
    'menubar.edit.plaintext',
    'menubar.about.website',
    'menubar.about.repo',
    'menubar.about.license',
    'menubar.settings.theme',
    'menubar.settings.preferences',
    'window.title',
    'window.button.complex',
    'window.button.edit',
    'window.button.add',
    'window.button.remove',
    'window.types',
    'popup.plaintext.title',
    'popup.plaintext.button.copy',
    'popup.edit.title',
    'popup.add.title',
    'popup.unsaved.title',
    'popup.unsaved.body.load',
    'popup.unsaved.body.close',
    'popup.unsaved.buttons',
    'popup.button.ok',
    'popup.button.save',
    'error.missingfile.title',
    'error.missingfile.body',
    'error.json.title',
    'error.json.body',
    'error.json.submessage.overwrite',
    'error.json.submessage.attempt',
    'error.eof.title',
    'error.eof.body',
    'error.permission.title',
    'error.permission.read.body',
    'error.permission.write.body', 
    'error.permission.submessage.noread',
    'error.generic.title',
    'error.generic.read.body',
    'error.generic.write.body',
    'error.generic.emptykey',
    'error.generic.dupekey',
    'contextmenu.save',
    'contextmenu.saveas',
    'contextmenu.open',
    'contextmenu.add',
    'contextmenu.remove',
    'contextmenu.plaintext',
    'settings.title',
    'settings.label.indent',
    'settings.label.extension',
    'settings.label.lang',
    'theme.title',
    'theme.label.global',
    'theme.warn.restart',
    'filepicker.filter.json',
]
# keys that need to be in list format, others should be strings
listKeys = [
    'popup.unsaved.buttons',
    'window.types',
]

# open and ensure the usability of the lang files
def loadMeta(file: str) -> dict | None:
    # open the file
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None
    
    # load the metadata
    try:
        commonName = data['common_name']
    except KeyError:
        return None

    return {file: commonName}

# load the JSON data and return the value of the lang key
def loadData(file: str) -> dict:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {'error': 'invalid_json'}
    except FileNotFoundError:
        return {'error': 'file_not_found'}
    except PermissionError:
        return {'error': 'permission_denied'}
    except Exception as e:
        return {'error': 'unknown_error', 'message': str(e)}

    if 'lang' not in data:
        return {'error': 'missing_key', 'key': 'lang'}
    
    for key in keys:
        # check to see if the key exists
        if key not in data['lang']:
            return {'error': 'missing_key', 'key': key}
        # check to make sure the key is the correct format
        elif key in listKeys:
            if not isinstance(data['lang'][key], list):
                return {'error': 'bad_key_type', 'key': key}
        elif not isinstance(data['lang'][key], str):
            return {'error': 'bad_key_type', 'key': key}
    
    return {'success': True, 'data': data['lang']}

# remove any language files with the same common name to avoid confusion
def removeDuplicates(langFiles):
    seen = {}
    for path, commonName in langFiles.items():
        if commonName not in seen or path.startswith('lang/'):
            seen[commonName] = path
    # Return in the format {filename: commonname}
    return {path: commonName for commonName, path in seen.items()}

# Define possible language file locations (installed and source directory)
langDirs = [
    os.path.join(RESOURCEDIR, 'lang'),  # Installed location
    'lang'  # Source directory (for development)
]
langFiles = dict()  # holds metadata and corresponding lang files

# Search for language files in both locations
for langPath in langDirs:
    if os.path.isdir(langPath):  # Check if the directory exists
        for file in glob.glob(os.path.join(langPath, '*.json')):
            meta = loadMeta(file)
            if meta != None:
                langFiles.update(meta)
