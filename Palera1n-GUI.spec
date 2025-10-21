# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# Metadata
app_name = 'Palera1n-GUI'
version = '1.0.6'
script_path = 'Palera1n-GUI.py'

# Platform detection
is_macos = sys.platform == 'darwin'
is_linux = sys.platform == 'linux'

# Platform-specific configurations
if is_macos:
    icon_file = 'images/icon.icns'
    binary_path = ('bin/macos/palera1n', 'bin/macos')
    # Hidden Cocoa + Foundation modules (PyObjC) - macOS only
    hiddenimports = collect_submodules('Cocoa') + collect_submodules('Foundation')
elif is_linux:
    icon_file = 'images/icon.png'  # Linux uses .png
    binary_path = ('bin/linux/palera1n', 'bin/linux')
    hiddenimports = []
else:
    print("ERROR: This application only supports macOS and Linux")
    sys.exit(1)

# Data files to embed
datas = [
    ('images/palera1n_gui.png', 'images'),
]

# Add platform-specific binary if it exists
if binary_path and os.path.exists(binary_path[0]):
    datas.append(binary_path)
else:
    print(f"Warning: Binary not found at {binary_path[0] if binary_path else 'unknown path'}")

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
    icon=icon_file if icon_file and os.path.exists(icon_file) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=app_name
)

# macOS-specific: Create .app bundle
if is_macos:
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
            'CFBundleIconFile': os.path.basename(icon_file),
            'CFBundleIdentifier': 'com.freqrider.palera1ngui',
            'CFBundlePackageType': 'APPL',
            'NSHighResolutionCapable': True,
            'NSPrincipalClass': 'NSApplication',

        }
    )