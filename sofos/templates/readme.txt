# to compile from qtDesigner:
pyuic5 untitled.ui -o output.py

# to compile qrc files:
pyrcc5 resource_file.qrc -o compiled_resource_file.py

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
