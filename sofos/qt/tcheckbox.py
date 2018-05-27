import PyQt5.QtWidgets as Qw
from .settings import MIN_HEIGHT


class TCheckbox(Qw.QCheckBox):
    """True or False field: 0 for unchecked , 2 for checked"""
    def __init__(self, val=False, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txtVal):
        self.setChecked(int(txtVal)) if txtVal else self.setChecked(False)

    def get(self):
        return self.checkState()
