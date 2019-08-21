Used for STEM Challenge. 
This shows how deadline can lead to lots of bad practices :'(


Tested on Ubuntu 18.04 and Lubuntu 19.04

Dependencies:
- Python3     - sudo apt install python3
- pip3        - sudo apt install python3-pip
- TkInter     - sudo apt install python3-tk
- virtualenv	- python3 -m pip install --user virtualenv
- OpenCV      - pip install opencv-python
- PySimpleGUI - pip install PySimpleGUI
- PySerial    - pip install pyserial
- opencv.zip	- https://mega.nz/#!RZMAAQiJ!v2gFDN5LQVbFyOr9Crn2Gdoqfgsv4YNz3NiCdf6UY64

Instructions: 
1. Install Python3, pip3, TkInter, and virtualenv
2. Create a folder for virtual environment named "environment"
3. Create a virtual environment named "env" via python3 -m venv env
4. Create a folder called "opencv" inside "environment"
5. Unzip the contents of opencv.zip to "opencv"
6. Activate virtual environment via source env/bin/activate
7. Install OpenCV, PySimpleGUI, PySerial via pip inside virtual environment
8. Run bimo.py by python3 bimo.py

Debug:
- File with test_ prefix is used to make sure each dependencies are installed.
- To know which serial port Arduino is using, use ls /dev/tty*
- If Arduino is not detected, use sudo usermod -a -G dialout $USER and re-login.

Screenshot:
![bimo](https://user-images.githubusercontent.com/25707231/63456254-15f95d80-c481-11e9-9ea0-70672962c851.jpeg)
