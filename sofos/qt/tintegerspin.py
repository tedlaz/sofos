import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc


class TIntegerSpin(Qw.QSpinBox):
    '''Integer values (eg 123)'''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimum(0)
        self.setMaximum(999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)

    def get(self):
        return self.value()

    def set(self, val):
        self.setValue(int(val)) if val else self.setValue(0)
