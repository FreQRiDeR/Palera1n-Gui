import subprocess
import sys
import os
from Cocoa import (
    NSApplication, NSWindow, NSButton, NSImageView, NSTextField,
    NSImage, NSMakeRect, NSBackingStoreBuffered,NSFont,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskResizable
)
from Foundation import NSObject, NSAutoreleasePool


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        pass


class Palera1nGUI:
    def __init__(self):
        self.app = NSApplication.sharedApplication()
        self.delegate = AppDelegate.alloc().init()
        self.app.setDelegate_(self.delegate)

        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(200.0, 100.0, 400.0, 400.0),
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
            "CREATE FAKEFS": "palera1n -cf",
            "DEVICE INFO": "palera1n -I",
            "GET PALERA1N": "print Go to: https://palera.in",
            "REMOVE JB": "palera1n --force-revert",
            "SAFE MODE -l": "palera1n -sl",
            "SAFE MODE -f": "palera1n -sf",
            "CLEAN FS": "palera1n -Cf",
            "EXIT RECOVERY": "palera1n -n",
            "VERSION": "palera1n --version"
        }

        self.add_header_image()
        self.create_buttons()
        self.add_footer_text()

    def add_header_image(self):
        image_path = resource_path("palera1n_gui.png")
        image = NSImage.alloc().initWithContentsOfFile_(image_path)
        if image:
            image_view = NSImageView.alloc().initWithFrame_(NSMakeRect(0, 280, 400, 130))
            image_view.setImage_(image)
            image_view.setImageScaling_(2)  # 2 = NSImageScaleProportionallyUpOrDown
            self.window.contentView().addSubview_(image_view)
        else:
            print("Image not loaded")

    def add_footer_text(self):
        # "by" label
        by_label = NSTextField.alloc().initWithFrame_(NSMakeRect(110, 30, 100, 20))
        by_label.setStringValue_("by")
        by_label.setEditable_(False)
        by_label.setBezeled_(False)
        by_label.setDrawsBackground_(False)
        by_label.setAlignment_(1)  # Center
        by_label.setFont_(NSFont.systemFontOfSize_(13))
        by_label.setSelectable_(False)

        # "FreQRiDeR" label
        author_label = NSTextField.alloc().initWithFrame_(NSMakeRect(135, 13, 100, 20))
        author_label.setStringValue_("FreQRiDeR")
        author_label.setEditable_(False)
        author_label.setBezeled_(False)
        author_label.setDrawsBackground_(False)
        author_label.setAlignment_(1)  # Center
        author_label.setFont_(NSFont.systemFontOfSize_(13))
        author_label.setSelectable_(False)

        self.window.contentView().addSubview_(by_label)
        self.window.contentView().addSubview_(author_label)



    def create_buttons(self):
        button_width = 150
        button_height = 30
        spacing_x = 30
        spacing_y = 10
        start_x = 35
        start_y = 260
        buttons_per_column = 6

        for index, (label, _) in enumerate(self.commands.items()):
            col = index // buttons_per_column
            row = index % buttons_per_column
            x = start_x + col * (button_width + spacing_x)
            y = start_y - row * (button_height + spacing_y)

            button = NSButton.alloc().initWithFrame_(NSMakeRect(x, y, button_width, button_height))
            button.setTitle_(label)
            button.setTarget_(self)
            button.setAction_("runCommand:")
            button.setTag_(index)
            self.window.contentView().addSubview_(button)

    def runCommand_(self, sender):
        index = sender.tag()
        label = list(self.commands.keys())[index]
        command = self.commands[label]

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
