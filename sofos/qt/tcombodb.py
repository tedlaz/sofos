import PyQt5.QtWidgets as Qw
import logging  # debug, info, warning, error, critical


class TComboDB(Qw.QComboBox):
    '''Combo'''
    def __init__(self, idv, model, parent):
        super().__init__(parent)
        self._parent = parent
        self._model = model
        self.populate()
        self.set(idv)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        """Dangerus if id_ out of index"""
        if id_:
            try:
                self.setCurrentIndex(self.id2index[int(id_)])
            except KeyError:
                logging.error('value %s is out of index', id_)

    def populate(self):
        """
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        vlist = self._model.select_all_deep()
        self.index2id = {}
        self.id2index = {}
        self.addItem('')
        self.index2id[0] = ''
        self.id2index[''] = 0
        for i, elm in enumerate(vlist['rows']):
            self.addItem(' '.join([str(j) for j in elm[1:]]))
            self.index2id[i+1] = elm[0]
            self.id2index[elm[0]] = i+1
