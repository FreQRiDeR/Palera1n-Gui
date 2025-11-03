import subprocess
import sys
import os
import webbrowser
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont, QAction
from PyQt6.QtCore import Qt, QKeyCombination
from PyQt6.QtGui import QKeySequence


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
        
        # Detect platform for terminal commands
        self.platform = sys.platform
        
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
            # Fallback to system PATH
            import shutil
            system_binary = shutil.which('palera1n')
            if system_binary:
                palera1n_path = system_binary
                print(f"Using system palera1n at: {palera1n_path}")
            else:
                print("Error: No palera1n binary found!")
        elif not os.access(palera1n_path, os.X_OK):
            print(f"Warning: Binary not executable at {palera1n_path}")
            # Try to make it executable
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
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Palera1n-GUI")
        self.setFixedSize(400, 450)
        
        # Set window icon
        icon_path = resource_path("images/icon.png")
        if os.path.exists(icon_path):
            from PyQt6.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
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
        
        # App menu
        app_menu = menubar.addMenu("App")
        
        about_action = QAction("About Palera1n-GUI", self)
        about_action.triggered.connect(self.open_about)
        app_menu.addAction(about_action)
        
        app_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        app_menu.addAction(quit_action)
        
        # Commands menu
        commands_menu = menubar.addMenu("Commands")
        
        shortcuts = {
            "HELP": "Ctrl+H",
            "ROOTLESS": "Ctrl+L",
            "ROOTFUL": "Ctrl+F",
            "SAFE MODE -l": "Ctrl+Shift+L",
            "SAFE MODE -f": "Ctrl+Shift+F",
            "PALERA1N INFO": "Ctrl+I",
            "DEVICE INFO": "Ctrl+Shift+I",
            "VERSION": "Ctrl+V",
            "EXIT RECOVERY": "Ctrl+E"
        }
        
        for label in self.commands.keys():
            action = QAction(label, self)
            if label in shortcuts:
                action.setShortcut(shortcuts[label])
            
            if label == "PALERA1N INFO":
                action.triggered.connect(lambda checked, l=label: self.open_url(l))
            else:
                action.triggered.connect(lambda checked, l=label: self.run_command(l))
            
            commands_menu.addAction(action)
    
    def add_header_image(self, layout):
        image_path = resource_path("images/palera1n_gui.png")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Scale image proportionally
            pixmap = pixmap.scaled(323, 102, Qt.AspectRatioMode.KeepAspectRatio, 
                                   Qt.TransformationMode.SmoothTransformation)
            
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)
        else:
            # Fallback text if image not found
            title_label = QLabel("Palera1n GUI")
            title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
        
        # Version label
        version_label = QLabel("v1.0.6")
        version_label.setFont(QFont("Arial", 11))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
    
    def create_buttons(self, layout):
        # Create grid layout for buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)
        
        buttons_per_column = 6
        
        for index, label in enumerate(self.commands.keys()):
            col = index // buttons_per_column
            row = index % buttons_per_column
            
            button = QPushButton(label)
            button.setMinimumHeight(30)
            button.setMaximumWidth(130)  # Limit button width
            
            if label == "PALERA1N INFO":
                button.clicked.connect(lambda checked, l=label: self.open_url(l))
            else:
                button.clicked.connect(lambda checked, l=label: self.run_command(l))
            
            grid_layout.addWidget(button, row, col)
        
        # Prevent columns from stretching
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
        command = self.commands[label]
        
        try:
            if self.platform == 'darwin':
                # macOS - use Terminal.app
                escaped_command = command.replace('\\', '\\\\').replace('"', '\\"')
                full_command = f'zsh -l -c "{escaped_command}"'
                full_command = full_command.replace('\\', '\\\\').replace('"', '\\"')
                
                apple_script = f'''
                tell application "Terminal"
                    do script "{full_command}"
                    activate
                end tell
                '''
                subprocess.Popen(['osascript', '-e', apple_script])
                
            elif self.platform == 'linux':
                # Linux - try common terminal emulators
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
                    # Fallback: show error
                    QMessageBox.warning(self, "Terminal Not Found", 
                                      "Could not find a suitable terminal emulator.\n"
                                      "Please install gnome-terminal, konsole, or xterm.")
                    
            elif self.platform == 'win32':
                # Windows - use cmd
                subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', command])
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch terminal:\n{e}")
    
    def open_url(self, label):
        url = self.commands[label]
        webbrowser.open(url)
    
    def open_about(self):
        webbrowser.open("https://github.com/FreQRiDeR/Palera1n-Gui/")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Palera1n-GUI")
    
    window = Palera1nGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()