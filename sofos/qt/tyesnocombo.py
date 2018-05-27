import PyQt5.QtWidgets as Qw


class TYesNoCombo(Qw.QComboBox):
    '''Yes/No Combo'''
    def __init__(self, val=0, noyes=['No', 'Yes'], parent=None):
        super().__init__(parent)
        self.addItem(noyes[0])
        self.addItem(noyes[1])
        self.set(val)

    def get(self):
        return self.currentIndex() != 0

    def set(self, val):
        if not val:
            val = 0
        idx = 0
        if int(val) != 0:
            idx = 1
        self.setCurrentIndex(idx)
