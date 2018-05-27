import PyQt5.QtWidgets as Qw


class TCombo(Qw.QComboBox):
    '''Combo'''
    def __init__(self, val=0, vlist=[], parent=None):
        super().__init__(parent)
        self.populate(vlist)
        self.set(val)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[id_])
        else:
            self.setCurrentIndex(0)

    def populate(self, vlist):
        """
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        self.index2id = {}
        self.id2index = {}
        for i, elm in enumerate(vlist):
            self.addItem('%s' % elm[1])
            self.index2id[i] = elm[0]
            self.id2index[elm[0]] = i
