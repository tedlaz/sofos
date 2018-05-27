import PyQt5.QtWidgets as Qw
from .settings import MIN_HEIGHT
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg


class TTextLine(Qw.QLineEdit):
    """Text Line Class"""
    def __init__(self, val='', parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txt):
        if txt is not None:
            self.setText(str(txt).strip())
        else:
            self.setText('')
        self.setCursorPosition(0)

    def get(self):
        return str(self.text()).strip()


class TInteger(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)

    def set(self, txt):
        if txt is None or txt == '':
            self.setText('0')
        else:
            self.setText(str(txt).strip())
        self.setCursorPosition(0)


class TIntegerKey(TInteger):
    '''Text field with numeric chars only left aligned.'''

    def set(self, txt):
        if txt is None or txt == '':
            self.setText('')
        else:
            self.setText(str(txt).strip())
        self.setCursorPosition(0)


class TTextlineNum(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))

    def set(self, txt):
        if txt is not None:
            self.setText(str(txt).strip())
        else:
            self.setText('')
        self.setCursorPosition(0)
