# to compile from qtDesigner:
pyuic5 untitled.ui -o output.py

# to compile qrc files:
pyrcc5 main.qrc -o main_rc.py

# file .qrc contains :

<!DOCTYPE RCC><RCC version="1.0">
<qresource>
    <file>images/copy.png</file>
    <file>images/cut.png</file>
    <file>images/new.png</file>
    <file>images/open.png</file>
    <file>images/paste.png</file>
    <file>images/save.png</file>
</qresource>
</RCC>

where images is the actual image directory.

Basic .travis.yml file:
language: python
python:
  - "3.6"
cache: pip
install: "pip install -r requirements.txt"
before_script:
  - "export DISPLAY=:99.0"
  - "sh -e /etc/init.d/xvfb start"
  - sleep 3
script: python -m unittest
- "/sbin/start-stop-daemon --start --quiet --pidfile /tmp/custom_xvfb_99.pid --make-pidfile --background --exec /usr/bin/Xvfb -- :99 -ac -screen 0 1280x1024x24"