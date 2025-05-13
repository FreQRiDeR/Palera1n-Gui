import subprocess
import sys
import os
import webbrowser
from Cocoa import (
    NSApplication, NSWindow, NSButton, NSImageView, NSTextField,
    NSImage, NSMakeRect, NSBackingStoreBuffered, NSFont,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskResizable
)
from Foundation import NSObject, NSAutoreleasePool


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


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
        self.window.setTitle_("Palera1n-GUI")
        self.window.makeKeyAndOrderFront_(None)

        palera1n_path = resource_path("bin/palera1n")
        self.commands = {
            "HELP": f'"{palera1n_path}" -h',
            "ROOTLESS": f'"{palera1n_path}" -l',
            "ROOTFUL": f'"{palera1n_path}" -f',
            "CREATE FAKEFS": f'"{palera1n_path}" -cf',
            "DEVICE INFO": f'"{palera1n_path}" -I',
            "PALERA1N INFO": "https://palera.in",
            "REMOVE JB": f'"{palera1n_path}" --force-revert',
            "SAFE MODE -l": f'"{palera1n_path}" -sl',
            "SAFE MODE -f": f'"{palera1n_path}" -sf',
            "CLEAN FS": f'"{palera1n_path}" -Cf',
            "EXIT RECOVERY": f'"{palera1n_path}" -n',
            "VERSION": f'"{palera1n_path}" --version'
        }

        self.add_header_image()
        self.create_buttons()
        self.add_footer_text()

    def add_header_image(self):
        image_path = resource_path("images/palera1n_gui.png")
        image = NSImage.alloc().initWithContentsOfFile_(image_path)
        if image:
            image_view = NSImageView.alloc().initWithFrame_(NSMakeRect(0, 280, 400, 130))
            image_view.setImage_(image)
            image_view.setImageScaling_(2)  # NSImageScaleProportionallyUpOrDown
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

        # "v1.0.3" label
        version_label = NSTextField.alloc().initWithFrame_(NSMakeRect(117, 285, 100, 20))
        version_label.setStringValue_("v1.0.3")
        version_label.setEditable_(False)
        version_label.setBezeled_(False)
        version_label.setDrawsBackground_(False)
        version_label.setAlignment_(1)  # Center
        version_label.setFont_(NSFont.systemFontOfSize_(10))
        version_label.setSelectable_(False)

        self.window.contentView().addSubview_(by_label)
        self.window.contentView().addSubview_(author_label)
        self.window.contentView().addSubview_(version_label)

    def create_buttons(self):
        button_width = 135
        button_height = 22
        spacing_x = 30
        spacing_y = 15
        start_x = 52
        start_y = 255
        buttons_per_column = 6

        for index, (label, _) in enumerate(self.commands.items()):
            col = index // buttons_per_column
            row = index % buttons_per_column
            x = start_x + col * (button_width + spacing_x)
            y = start_y - row * (button_height + spacing_y)

            button = NSButton.alloc().initWithFrame_(NSMakeRect(x, y, button_width, button_height))
            button.setTitle_(label)
            button.setTarget_(self)
            if label == "PALERA1N INFO":
                button.setAction_("openURL:")
            else:
                button.setAction_("runCommand:")
            button.setTag_(index)
            self.window.contentView().addSubview_(button)

    def runCommand_(self, sender):
        index = sender.tag()
        label = list(self.commands.keys())[index]
        command = self.commands[label]

        # Construct AppleScript safely, handling quotes
        escaped_command = command.replace('\\', '\\\\').replace('"', '\\"')
        full_command = f'zsh -l -c "{escaped_command}"'
        full_command = full_command.replace('\\', '\\\\').replace('"', '\\"')

        apple_script = f'''
        tell application "Terminal"
            do script "{full_command}"
            activate
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', apple_script])
        except Exception as e:
            print(f"Error launching Terminal: {e}")

    def openURL_(self, sender):
        index = sender.tag()
        label = list(self.commands.keys())[index]
        url = self.commands[label]
        webbrowser.open(url)

    def run(self):
        self.app.run()


if __name__ == "__main__":
    pool = NSAutoreleasePool.alloc().init()
    gui = Palera1nGUI()
    gui.run()
