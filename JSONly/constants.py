# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# This file defines certain constants that will need to be used by other parts of the program
import os
import sys
import inspect

OS = sys.platform

frame = inspect.stack()[-1]  # Get the most recent frame (main file's frame)
mainFile = frame[0].f_globals["__file__"]
FILEDIR = os.path.abspath(os.path.dirname(mainFile))
MODIFIER = 'Control'

# set OS-dependant constants
match OS:
    case'linux':
        packaging = 'source'  # be sure to set this variable based on how the app is packaged.The setup.sh script should automatically set this.
        CONFIGDIR = os.getenv(
            'XDG_CONFIG_HOME',
            os.path.join(os.getenv('HOME', ''),
            '.config')
        )
        DATADIR = os.getenv(
            'XDG_DATA_HOME',
            os.path.join(os.getenv('HOME', ''),'.local', 'share')
        )
        if packaging == 'source': # running from source
            RESOURCEDIR = FILEDIR
        elif packaging == 'system': # installed with the system's package manager (APT, DNF, etc.)
            RESOURCEDIR = '/usr/share/JSONly/'
        elif packaging == 'appimage': # running in an appimage
            RESOURCEDIR = os.path.join(
                os.path.dirname(os.path.dirname(sys.executable)),
                'share',
                'JSONly'
            )
        else:
            RESOURCEDIR = FILEDIR
    case 'darwin': # MacOS
        CONFIGDIR = os.path.join(
            os.getenv("HOME", ""),
            "Library",
            "Application Support"
        )
        DATADIR = CONFIGDIR
        if getattr(sys, 'frozen', False):
            basePath = os.path.dirname(os.path.dirname(sys.executable))
            RESOURCEDIR = os.path.join(basePath, 'Resources')
        else:
            RESOURCEDIR = FILEDIR
        MODIFIER = 'Command'
    case 'win32': # before we get started, why does Windows just have to be different and use %VAR% instead of $VAR like other systems?
        CONFIGDIR = os.getenv(
            "LOCALAPPDATA",
            os.path.join(
                os.getenv("USERPROFILE", ""),
                "AppData",
                "Local"
            )
        )
        DATADIR = CONFIGDIR
        if getattr(sys, 'frozen', False):
            basePath = sys._MEIPASS
            RESOURCEDIR = os.path.join(basePath, 'resources')
        else:
            RESOURCEDIR = FILEDIR
    case 'FreeBSD':
        CONFIGDIR = os.path.join(os.getenv('HOME'), '.config')
        DATADIR = os.path.join(os.getenv('HOME'), '.local/share')
        RESOURCEDIR = FILEDIR
    case _:  # anything other
        CONFIGDIR = '.'
        DATADIR = '.'
CONFIGDIR = os.path.join(CONFIGDIR, 'JSONly')
DATADIR = os.path.join(DATADIR, 'JSONly')
VERSION = '1.4.1'  # current application version
LINKS = {
    'repo': 'https://github.com/DudenessBoy/JSONly',
    'version': 'https://dudenessboy.github.io/JSONly/version.txt',
    'version_beta': 'https://dudenessboy.github.io/JSONly/beta_version.txt',
    'download': 'https://dudenessboy.github.io/JSONly/download',
    'download_beta': 'https://dudenessboy.github.io/JSONly/download/beta.html',
    'website': 'https://dudenessboy.github.io/JSONly',
    'license': 'https://opensource.org/license/mit'
}
