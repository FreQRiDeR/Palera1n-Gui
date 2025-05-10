# Palera1n-GUI.spec
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.datastruct import TOC
from PyInstaller.building.osx import BUNDLE

a = Analysis(
    ['Palera1n-GUI.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bin/palera1n', 'bin'),
        ('images/palera1n_gui.png', 'images'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Palera1n-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False
)

app = BUNDLE(
    exe,
    name='Palera1n-GUI.app',
    icon='images/icon.icns',
    bundle_identifier='com.freqrider.palera1ngui',
    info_plist={
        'CFBundleName': 'Palera1n-GUI',
        'CFBundleDisplayName': 'Palera1n-GUI',
        'CFBundleIdentifier': 'com.freqrider.palera1ngui',
        'CFBundleVersion': '1.0.2',
        'CFBundleShortVersionString': '1.0.2',
        'NSHighResolutionCapable': 'True'
    }
)
