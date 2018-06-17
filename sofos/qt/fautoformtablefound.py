import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .fautoformtable import AutoFormTable


class AutoFormTableFound(AutoFormTable):
    def __init__(self, model, search_string, parent=None):
        self.search_string = search_string
        super().__init__(model, parent)
        self.tbl.cellDoubleClicked.disconnect(self._edit_record)
        self.tbl.cellDoubleClicked.connect(self.accept)
        # keyv = "FormSize/%s" % self.model.table_name()
        # self.resize(self.settings.value(keyv, Qc.QSize(300, 240)))
        self.resize(Qc.QSize(640, 480))

    def _get_data(self):
        return self.model.search_deep(self.search_string)

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection'''
        if ev.key() in (Qc.Qt.Key_Enter, Qc.Qt.Key_Return):
            self.accept()
        Qw.QDialog.keyPressEvent(self, ev)
