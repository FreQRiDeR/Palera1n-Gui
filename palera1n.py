import subprocess
from Cocoa import (
    NSApplication, NSWindow, NSButton,
    NSMakeRect, NSBackingStoreBuffered,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskResizable
)
from Foundation import NSObject, NSAutoreleasePool


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        pass


class Palera1nGUI:
    def __init__(self):
        self.app = NSApplication.sharedApplication()
        self.delegate = AppDelegate.alloc().init()
        self.app.setDelegate_(self.delegate)

        # Window size for 2 columns and 5 rows
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(200.0, 100.0, 400.0, 300.0),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        self.window.setTitle_("Palera1n Launcher")
        self.window.makeKeyAndOrderFront_(None)

        self.commands = {
            "HELP": "palera1n -h",
            "ROOTLESS": "palera1n -l",
            "ROOTFUL": "palera1n -f",
            "CLEAN FS": "palera1n -C",
            "CREATE FAKEFS": "palera1n -cf",
            "GET PALERA1N": "print Go to: https://palera.in",
            "REMOVE JB": "palera1n --force-revert",
            "SAFE MODE -l": "palera1n -sl",
            "SAFE MODE -f": "palera1n -sf",
            "DEVICE INFO": "palera1n -I",
            "EXIT RECOV": "palera1n -n",
            "VERSION": "palera1n --version"

        }

        self.create_buttons()

    def create_buttons(self):
        button_width = 150
        button_height = 30
        spacing_x = 30
        spacing_y = 10
        start_x = 40
        start_y = 240
        buttons_per_column = 6

        for index, (label, _) in enumerate(self.commands.items()):
            col = index // buttons_per_column
            row = index % buttons_per_column
            x = start_x + col * (button_width + spacing_x)
            y = start_y - row * (button_height + spacing_y)

            button = NSButton.alloc().initWithFrame_(NSMakeRect(
                x, y, button_width, button_height
            ))
            button.setTitle_(label)
            button.setTarget_(self)
            button.setAction_("runCommand:")
            button.setTag_(index)
            self.window.contentView().addSubview_(button)

    def runCommand_(self, sender):
        index = sender.tag()
        label = list(self.commands.keys())[index]
        command = self.commands[label]

        # Escape quotes for AppleScript
        command_escaped = command.replace('"', '\\"')

        applescript = f'''
        tell application "Terminal"
            do script "zsh -l -c \\"{command_escaped}\\""
            activate
        end tell
        '''

        try:
            subprocess.run(['osascript', '-e', applescript])
        except Exception as e:
            print(f"Error launching Terminal: {e}")

    def run(self):
        self.app.run()


if __name__ == "__main__":
    pool = NSAutoreleasePool.alloc().init()
    gui = Palera1nGUI()
    gui.run()
