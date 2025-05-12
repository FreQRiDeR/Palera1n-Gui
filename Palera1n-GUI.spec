# Palera1n-GUI.spec
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.datastruct import TOC

block_cipher = None

a = Analysis(
    ['Palera1n-GUI.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('bin/palera1n', 'bin'),
        ('images/palera1n_gui.png', 'images'),
        ('images/icon.icns', 'images')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=False,
    icon='images/icon.icns'
    plist='Info.plist'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Palera1n-GUI'
)
