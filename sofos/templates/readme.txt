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
cache: pip
python:
  - "3.6"
install:
  - pip install -q pyqt5==5.9.2  **** Be carefull version 5.10 gives segmentation faults
  - pip install coveralls
  - pip install codecov
script: xvfb-run coverage run -m unittest
after_success:
  - coveralls
  - codecov