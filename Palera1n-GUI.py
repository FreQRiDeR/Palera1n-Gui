import subprocess
import sys
import os
import webbrowser
import shutil
from pathlib import Path
from functools import partial
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QGridLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont, QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QEvent

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class Palera1nGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.platform = sys.platform
        print("DEBUG: Palera1nGUI.__init__() starting...")

        # Platform-specific binary path
        if self.platform == 'darwin':
            palera1n_path = resource_path("bin/macos/palera1n")
        elif self.platform == 'linux':
            palera1n_path = resource_path("bin/linux/palera1n")
        elif self.platform == 'win32':
            palera1n_path = resource_path("bin/windows/palera1n.exe")
        else:
            palera1n_path = resource_path("bin/palera1n")

        # Verify binary exists and is executable
        if not os.path.exists(palera1n_path):
            print(f"Warning: Bundled binary not found at {palera1n_path}")
            system_binary = shutil.which('palera1n')
            if system_binary:
                palera1n_path = system_binary
                print(f"Using system palera1n at: {palera1n_path}")
            else:
                print("Error: No palera1n binary found!")
        elif not os.access(palera1n_path, os.X_OK):
            print(f"Warning: Binary not executable at {palera1n_path}")
            try:
                os.chmod(palera1n_path, 0o755)
                print(f"Made binary executable: {palera1n_path}")
            except Exception as e:
                print(f"Could not make binary executable: {e}")

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

        self.shortcuts = {
            "HELP": "Ctrl+H",
            "ROOTLESS": "Ctrl+L",
            "ROOTFUL": "Ctrl+F",
            "CREATE FAKEFS": "Ctrl+Shift+F",
            "DEVICE INFO": "Ctrl+I",
            "PALERA1N INFO": "Ctrl+Shift+I",
            "REMOVE JB": "Ctrl+R",
            "SAFE MODE -l": "Ctrl+Alt+L",
            "SAFE MODE -f": "Ctrl+Alt+F",
            "CLEAN FS": "Ctrl+Shift+C",
            "EXIT RECOVERY": "Ctrl+E",
            "VERSION": "Ctrl+V"
        }

        self.init_ui()
        print("DEBUG: Palera1nGUI.__init__() complete")

    def create_command_action(self, label):
        action = QAction(label, self)
        action.setObjectName(f"cmd_{label}")
        action.setMenuRole(QAction.MenuRole.NoRole)
        if label in self.shortcuts:
            action.setShortcut(QKeySequence(self.shortcuts[label]))
        if label == "PALERA1N INFO":
            action.triggered.connect(lambda checked=False, label=label: self.open_url(label))
        else:
            action.triggered.connect(lambda checked=False, label=label: self.run_command(label))
        return action

    def init_ui(self):
        self.setWindowTitle("Palera1n-GUI")
        self.setFixedSize(400, 450)

        icon_path = resource_path("images/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.setup_menu_bar()
        self.add_header_image(main_layout)
        self.create_buttons(main_layout)
        self.add_footer(main_layout)

    def setup_menu_bar(self):
        menubar = self.menuBar()

        # ===== APP MENU =====
        app_menu = menubar.addMenu("&File")

        about_action = QAction("&About Palera1n-GUI", self)
        about_action.triggered.connect(self.open_about)
        app_menu.addAction(about_action)
        app_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setObjectName("app_quit")
        quit_action.setMenuRole(QAction.MenuRole.QuitRole)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(QApplication.quit)
        app_menu.addAction(quit_action)

        # ===== COMMANDS MENU =====
        commands_menu = menubar.addMenu("&Commands")
        for label in self.commands.keys():
            action = self.create_command_action(label)
            commands_menu.addAction(action)

    def add_header_image(self, layout):
        image_path = resource_path("images/palera1n_gui.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                380, 120, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)
        else:
            title_label = QLabel("Palera1n GUI")
            title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)

        version_label = QLabel("v1.0.6")
        version_label.setFont(QFont("Arial", 9))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

    def create_buttons(self, layout):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        buttons_per_column = 6

        for index, label in enumerate(self.commands.keys()):
            col = index // buttons_per_column
            row = index % buttons_per_column
            button = QPushButton(label)
            button.setMinimumHeight(32)
            button.setMaximumWidth(130)
            if label == "PALERA1N INFO":
                button.clicked.connect(lambda checked=False, label=label: self.open_url(label))
            else:
                button.clicked.connect(lambda checked=False, label=label: self.run_command(label))
            grid_layout.addWidget(button, row, col)

        grid_layout.setColumnStretch(0, 0)
        grid_layout.setColumnStretch(1, 0)
        layout.addLayout(grid_layout)

    def add_footer(self, layout):
        layout.addStretch()
        by_label = QLabel("by")
        by_label.setFont(QFont("Arial", 11))
        by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(by_label)

        author_label = QLabel("FreQRiDeR")
        author_label.setFont(QFont("Arial", 11))
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

    def run_command(self, label):
        sender = self.sender()
        if sender and sender.objectName() == "app_quit":
            print("DEBUG: run_command ignored — triggered by Quit action")
            return

        if QApplication.instance().closingDown():
            print(f"DEBUG: Ignoring command '{label}' during shutdown")
            return

        command = self.commands[label]
        print(f"DEBUG: run_command triggered for '{label}'")

        try:
            if self.platform == 'darwin':
                safe_command = command.replace('"', '\\"')
                apple_script = f'''
                tell application "Terminal"
                    do script "zsh -l -c \\"{safe_command}\\""
                    activate
                end tell
                '''
                subprocess.Popen(['osascript', '-e', apple_script])
            elif self.platform == 'linux':
                terminals = [
                    ['gnome-terminal', '--', 'bash', '-c', f'{command}; read -p "Press Enter to close..."'],
                    ['konsole', '-e', 'bash', '-c', f'{command}; read -p "Press Enter to close..."'],
                    ['xterm', '-e', f'bash -c \'{command}; read -p "Press Enter to close..."\' '],
                    ['x-terminal-emulator', '-e', 'bash', '-c', f'{command}; read -p "Press Enter to close..."']
                ]
                for term_cmd in terminals:
                    try:
                        subprocess.Popen(term_cmd)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    QMessageBox.warning(self, "Terminal Not Found",
                        "Could not find a suitable terminal emulator.\n"
                        "Please install gnome-terminal, konsole, or xterm.")
            elif self.platform == 'win32':
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', command])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch terminal:\n{e}")

    def open_url(self, label):
        webbrowser.open(self.commands[label])

    def open_about(self):
        webbrowser.open("https://github.com/FreQRiDeR/Palera1n-Gui/")

    def event(self, e):
        if e.type() == QEvent.Type.Close:
            print("DEBUG: Close event detected in event()")
        if e.type() == QEvent.Type.Quit:
            print("DEBUG: Quit event detected in event()")
        return super().event(e)

    def closeEvent(self, event):
        print("DEBUG: closeEvent called!")
        for action in self.findChildren(QAction):
            if action.objectName().startswith("cmd_"):
                try:
                    action.triggered.disconnect()
                    print(f"DEBUG: Disconnected {action.objectName()}")
                except Exception as e:
                    print(f"DEBUG: Failed to disconnect {action.objectName()}: {e}")
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Palera1n-GUI")
    app.aboutToQuit.connect(lambda: print("DEBUG: aboutToQuit signal triggered!"))
    window = Palera1nGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
