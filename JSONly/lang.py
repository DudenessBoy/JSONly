# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

import json
import glob
import os
from JSONly.constants import *

default = os.path.join(RESOURCEDIR, 'lang', 'en.json')  # default language file name

# a list of all keys that should be present in the lang file
keys = [
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
    'popup.plaintext.title',
    'popup.plaintext.button.copy',
    'popup.edit.title',
    'popup.add.title',
    'popup.unsaved.title',
    'popup.unsaved.body.load',
    'popup.unsaved.body.close',
    'popup.unsaved.buttons',
    'popup.update.title',
    'popup.update.body',
    'popup.update.buttons',
    'popup.button.ok',
    'popup.button.save',
    'popup.beta_warning.title',
    'popup.beta_warning.body',
    'popup.beta_warning.buttons',
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
    'settings.label.update',
    'settings.checkbox.enable_update',
    'settings.checkbox.beta_channel',
    'theme.title',
    'theme.label.global',
    'theme.warn.restart',
    'theme.option.dark',
    'theme.option.light',
    'theme.option.auto',
    'filepicker.filter.json',
]
# keys that need to be in list format, others should be strings
# this also contains the number of values that should be in each list
listKeys = {
    'popup.unsaved.buttons': 3,
    'window.types': 7,
    'popup.beta_warning.buttons': 2,
    'popup.update.buttons': 2,
}

# return a version of the language dictionary using the keys as values.
# this is useful for when the file is corrupted or missing.
def useKeys(message: str) -> None:
    print(f'{message} Using the language keys instead.')
    return dict(zip(keys, keys))

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

    return ({commonName: file}, {file: commonName})

# load the JSON data and return the value of the lang key
def loadData(file: str) -> dict:
    data = dict()
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data['lang'] = useKeys('The default language file contains JSON syntax errors.')
    except FileNotFoundError:
        if file != default:
            return loadData(default)
        else:
            data['lang'] = useKeys('The default language file could not be found.')
    except PermissionError:
        data['lang'] = useKeys('The default language file contains insufficient permissions.')
    except Exception as e:
        data['lang'] = useKeys(f'There was an error processing the default lang file:\n\
            {str(e)}\n')
    
    if 'lang' not in data:
        lang = useKeys('Language data was not found in the default lang file.')
    
    for key in keys:
        # check to see if the key exists, if not, assign the key as the value
        if key not in data['lang']:
            data['lang'][key] = key
        # check to make sure the key is the correct format
        if key in listKeys.keys():
            length = len(data['lang'][key])
            if not isinstance(data['lang'][key], list):
                data['lang'][key] = []
                for i in range(listKeys[key]):
                    data['lang'][key].append(f'{key}.{i}')
            elif length != listKeys[key]:
                if length > listKeys[key]:
                    data['lang'][key] = data['lang'][key][:listKeys[key]]
                else:
                    missing = listKeys[key] - len(data['lang'][key])
                    for i in range(listKeys[key] - missing, listKeys[key]):
                        data['lang'][key].append(f'{key}.{i}')
        elif not isinstance(data['lang'][key], str):
            data['lang'][key] = str(data['lang'][key])
    
    return data['lang']

langPath = os.path.join(RESOURCEDIR, 'lang')
langNames = dict()  # holds metadata and corresponding lang files
langFiles = dict()

# Search for language files
if os.path.isdir(langPath):  # Check if the directory exists
    for file in glob.glob(os.path.join(langPath, '*.json')):
        meta = loadMeta(file)
        if meta != None:
            langNames.update(meta[0])
            langFiles.update(meta[1])
