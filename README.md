<div align="center">
             <img src="/images/palera1n.png" width="1280" />
             <h1>PALERA1N GUI APP</h1>
</div>

PALERA1N GUI WRITTEN IN PYTHON

* For macOS, Debian based Linux
* Launches palera1n commands in terminal.
* Now with built-in palera1n executable! (v1.0.2)
* Now with built-in Python Libraries! (v1.0.3)
* Truly a stand-alone app now. 
* ⛔ macOS Gatekeeper & Unsigned Apps...
    Gatekeeper will still show a warning, since it’s not notarized.
    Users can bypass this by right-clicking the app and choosing "Open", then confirming the prompt.
  
* To run the project from source, from working directory:

```sh
# Move into project directory
cd ~/Palera1n-GUI
# Create Python 3.13 venv. From working directory, run:
python3.13 -m venv venv # your path may vary
# Activate venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Run python script
python3 Palera1n-GUI.py
```
* To build app from source yourself:

```sh
# Move into project directory
cd ~/Palera1n-GUI
# Create Python 3.13 venv. From working directory, run:
python3.13 -m venv venv # your path may vary
# Activate venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Create the pyinstaller based Application
python -m PyInstaller Palera1n-GUI.spec
# Open build folder
open /dist/
# To create .deb Linux package, run:
./Palera1n-GUI_build.sh
# To install deb, if you wish, run:
sudo dpkg -i palera1n-gui_1.0.6.deb
```

* Once done, you'll find the application generated at `/dist/Palera1n-GUI.app`

* By FreQRiDeR and ChatGPT. (Mostly ChatGPT! LOL)


<div align="center">
             <img src="/images/window.png" width="700" />
             
</div>
