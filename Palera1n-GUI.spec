# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# Metadata
app_name = 'Palera1n-GUI'
version = '1.0.3'
script_path = 'Palera1n-GUI.py'
icon_file = 'images/icon.icns'

# Data files to embed
datas = [
    ('images/palera1n_gui.png', 'images'),
    ('bin/palera1n', 'bin'),
]

# Hidden Cocoa + Foundation modules (PyObjC)
hiddenimports = collect_submodules('Cocoa') + collect_submodules('Foundation')

block_cipher = None

a = Analysis(
    [script_path],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_file,
)

coll = COLLECT(
    exe,  # <- Use EXE here instead of BUNDLE
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=app_name
)

app = BUNDLE(
    coll,
    name=f'{app_name}.app',
    icon=icon_file,
    bundle_identifier='com.freqrider.palera1ngui',
    info_plist={
        'CFBundleName': app_name,
        'CFBundleDisplayName': app_name,
        'CFBundleGetInfoString': f"{app_name} by FreQRiDeR",
        'CFBundleVersion': version,
        'CFBundleShortVersionString': version,
        'NSHighResolutionCapable': True,
    }
)
