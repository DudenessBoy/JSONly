# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

from setuptools import setup

APP = ['main.pyw']
DATA_FILES = [
    ('', ['resources/icon.icns', 'resources/doc/BSD-3-Clause.txt', '../../LICENSE', '../../icon.png']),
    ('lang', [
        '../../lang/en.json',
        '../../lang/es.json',
        ]
     )

]
OPTIONS = {
    'argv_emulation': False,
    'packages': ['JSONly', 'customtkinter', 'CTkListbox', 'plyer', 'pyperclip'],
    'iconfile': 'resources/icon.icns',
    'excludes': 'setuptools',
    'plist': {
        'CFBundleName': 'JSONly',
        'CFBundleVersion': '1.4.0',
        'CFBundleShortVersionString': '1.4',
        'NSHighResolutionCapable': True
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
