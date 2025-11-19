import subprocess
import sys
import os
import webbrowser
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QGridLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont, QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class Palera1nGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Detect platform for terminal commands
        self.platform = sys.platform

        # Platform-specific binary path
        if self.platform == 'darwin':
            palera1n_path = resource_path("bin/macos/palera1n")
        elif self.platform == 'linux':
            palera1n_path = resource_path("bin/linux/palera1n")
        else:
            palera1n_path = resource_path("bin/palera1n")

        # Verify binary exists and is executable
        if not os.path.exists(palera1n_path):
            print(f"Warning: Bundled binary not found at {palera1n_path}")
            import shutil
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

        # Commands dictionary (order preserved)
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
            "VERSION": f'"{palera1n_path}" --version',
            "EXIT RECOVERY": f'"{palera1n_path}" -n'
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Palera1n-GUI")
        self.setFixedSize(400, 450)

        # Set window icon
        icon_path = resource_path("images/icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Setup menu bar
        self.setup_menu_bar()

        # Header image
        self.add_header_image(main_layout)

        # Buttons grid
        self.create_buttons(main_layout)

        # Footer
        self.add_footer(main_layout)

    def setup_menu_bar(self):
        menubar = self.menuBar()
        if self.platform == 'darwin':
            # Ensure native macOS menu bar for proper ⌘ glyph rendering
            menubar.setNativeMenuBar(True)

        # App menu
        app_menu = menubar.addMenu("App")

        about_action = QAction("About Palera1n-GUI", self)
        about_action.triggered.connect(self.open_about)
        if self.platform == 'darwin':
            about_action.setMenuRole(QAction.MenuRole.AboutRole)
        app_menu.addAction(about_action)

        app_menu.addSeparator()

        # Quit action (preserved exactly as in your last script)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        if self.platform == 'darwin':
            quit_action.setMenuRole(QAction.MenuRole.QuitRole)
            quit_action.setShortcut(QKeySequence.StandardKey.Quit)  # ⌘Q
        else:
            quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        app_menu.addAction(quit_action)

        # Commands menu
        commands_menu = menubar.addMenu("Commands")

        # macOS: use Meta (⌘) strings; Linux: Ctrl strings
        if self.platform == 'darwin':
            shortcut_map = {
                "HELP": QKeySequence("Meta+H"),
                "ROOTLESS": QKeySequence("Meta+L"),
                "ROOTFUL": QKeySequence("Meta+F"),
                "SAFE MODE -l": QKeySequence("Meta+Shift+L"),
                "SAFE MODE -f": QKeySequence("Meta+Shift+F"),
                "PALERA1N INFO": QKeySequence("Meta+I"),
                "DEVICE INFO": QKeySequence("Meta+Shift+I"),
                "VERSION": QKeySequence("Meta+V"),
                # EXIT RECOVERY assigned explicitly below
            }
        else:
            shortcut_map = {
                "HELP": QKeySequence("Ctrl+H"),
                "ROOTLESS": QKeySequence("Ctrl+L"),
                "ROOTFUL": QKeySequence("Ctrl+F"),
                "SAFE MODE -l": QKeySequence("Ctrl+Shift+L"),
                "SAFE MODE -f": QKeySequence("Ctrl+Shift+F"),
                "PALERA1N INFO": QKeySequence("Ctrl+I"),
                "DEVICE INFO": QKeySequence("Ctrl+Shift+I"),
                "VERSION": QKeySequence("Ctrl+V"),
            }

        # Add all commands except EXIT RECOVERY (explicitly controlled)
        for label in self.commands.keys():
            if label == "EXIT RECOVERY":
                continue

            action = QAction(label, self)
            if self.platform == 'darwin':
                action.setMenuRole(QAction.MenuRole.NoRole)  # keep in Commands, never in App menu

            if label in shortcut_map:
                action.setShortcut(shortcut_map[label])

            if label == "PALERA1N INFO":
                action.triggered.connect(lambda checked=False, l=label: self.open_url(l))
            else:
                action.triggered.connect(lambda checked=False, l=label: self.run_command(l))

            commands_menu.addAction(action)

        # EXIT RECOVERY – explicit, with NoRole to prevent collisions
        recovery_action = QAction("EXIT RECOVERY", self)
        recovery_action.setMenuRole(QAction.MenuRole.NoRole)
        if self.platform == 'darwin':
            recovery_action.setShortcut(QKeySequence("Meta+R"))  # ⌘R
        else:
            recovery_action.setShortcut(QKeySequence("Ctrl+R"))
        recovery_action.triggered.connect(lambda checked=False: self.run_command("EXIT RECOVERY"))
        commands_menu.addAction(recovery_action)

    def add_header_image(self, layout: QVBoxLayout):
        image_path = resource_path("images/palera1n_gui.png")

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(
                323, 102,
                Qt.AspectRatioMode.KeepAspectRatio,
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
        version_label.setFont(QFont("Arial", 11))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

    def create_buttons(self, layout: QVBoxLayout):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)

        buttons_per_column = 6

        button_style = """
            QPushButton {
                background-color: #505050;
                color: white;
                border: 1px solid #606060;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
        """

        for index, label in enumerate(self.commands.keys()):
            col = index // buttons_per_column
            row = index % buttons_per_column

            button = QPushButton(label)
            button.setMinimumHeight(20)
            button.setMinimumWidth(120)
            button.setMaximumWidth(120)
            button.setStyleSheet(button_style)

            if label == "PALERA1N INFO":
                button.clicked.connect(lambda checked=False, l=label: self.open_url(l))
            else:
                button.clicked.connect(lambda checked=False, l=label: self.run_command(l))

            grid_layout.addWidget(button, row, col)

        grid_layout.setColumnStretch(0, 0)
        grid_layout.setColumnStretch(1, 0)

        layout.addLayout(grid_layout)

    def add_footer(self, layout: QVBoxLayout):
        layout.addStretch()

        by_label = QLabel("by")
        by_label.setFont(QFont("Arial", 11))
        by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(by_label)

        author_label = QLabel("FreQRiDeR")
        author_label.setFont(QFont("Arial", 11))
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

    def run_command(self, label: str):
        command = self.commands[label]

        try:
            if self.platform == 'darwin':
                # macOS - use Terminal.app; minimal escaping for predictability
                escaped = command.replace('\\', '\\\\').replace('"', '\\"')
                zsh_cmd = f'zsh -l -c "{escaped}"'
                zsh_cmd = zsh_cmd.replace('\\', '\\\\').replace('"', '\\"')

                apple_script = f'''
                tell application "Terminal"
                    do script "{zsh_cmd}"
                    activate
                end tell
                '''
                subprocess.Popen(['osascript', '-e', apple_script])

            elif self.platform == 'linux':
                terminals = [
                    ['gnome-terminal', '--', 'bash', '-c', f'{command}; read -p "Press Enter to close..."'],
                    ['konsole', '-e', 'bash', '-c', f'{command}; read -p "Press Enter to close..."'],
                    ['xterm', '-e', f'bash -c \'{command}; read -p "Press Enter to close..."\''],
                    ['x-terminal-emulator', '-e', 'bash', '-c', f'{command}; read -p "Press Enter to close..."']
                ]

                for term_cmd in terminals:
                    try:
                        subprocess.Popen(term_cmd)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    QMessageBox.warning(
                        self,
                        "Terminal Not Found",
                        "Could not find a suitable terminal emulator.\n"
                        "Please install gnome-terminal, konsole, or xterm."
                    )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch terminal:\n{e}")

    def open_url(self, label: str):
        url = self.commands[label]
        webbrowser.open(url)

    def open_about(self):
        webbrowser.open("https://github.com/FreQRiDeR/Palera1n-Gui/")


def main():
    # Ensure native menubar and correct Command glyph mapping on macOS
    if sys.platform == 'darwin':
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_MacDontSwapCtrlAndMeta, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Palera1n-GUI")

    window = Palera1nGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
