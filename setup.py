from setuptools import setup

APP = ['Palera1n-Gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile':'icon.icns',
    'plist': {
        'CFBundleName': 'Palera1n Launcher',
        'CFBundleDisplayName': 'Palera1n Launcher',
        'CFBundleIdentifier': 'com.example.palera1nlauncher',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
        'LSUIElement': False,  # Set to True if you want no Dock icon
    },
    'packages': [],
    'includes': ['Cocoa', 'Foundation']
}

setup(
    app=APP,
    name='Palera1n Launcher',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
