# -*- mode: python ; coding: utf-8 -*-

# Copyright (c) 2025 Luke Moyer
# Licensed under the MIT License. See LICENSE file for details.

# This is the PyInstaller spec file for compiling JSONly to a .exe file

a = Analysis(
    ['..\\main.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.abspath('..\\LICENSE'), 'resources'),
        (os.path.abspath('..\\lang'), 'resources\\lang'),
        (os.path.abspath('..\\icon.png'), 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JSONly',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
