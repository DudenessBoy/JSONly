from setuptools import setup

APP = ['main.pyw']
DATA_FILES = [
    ('resources', ['resources/icon.icns']),
    ('resources/doc', ['MIT.txt', 'BSD-3-Clause.txt', '../../LICENSE', '../../PSFL.txt'])
]
OPTIONS = {
    'packages': ['JSONly', 'customtkinter', 'CTkListbox', 'plyer', 'pyperclip']
    'iconfile': 'resources/icon.icns'
    'plist': {
        'CFBundleName': 'JSONly',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': True
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
