'''
pyqt controls
'''
# import datetime
# import decimal
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .widget_selector import wselector
from .settings import CONFIRMATIONS
from .ttextline import TIntegerKey


class MasterDetail(Qw.QDialog):
    val_updated = Qc.pyqtSignal(str)

    def __init__(self, master, detail, key, idv=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self._set(master, detail, key, idv)
        self._wtitle()
        self._create_layouts()
        self._create_Buttons()
        self._create_fields()
        self.populate()

    def _wtitle(self):
        self.setWindowTitle('{}: {}'.format(
            self.master.table_label(), self._id if self._id else 'New record'))

    def _set(self, master, detail, key, idv):
        self._id = idv
        self.master = master
        self.detail = detail
        self.key = key
        self.mwidgets = {}
        self.dwidgets = []

    def _create_layouts(self):
        self.main_layout = Qw.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.master_layout = Qw.QFormLayout()
        self.main_layout.addLayout(self.master_layout)
        self.detail_layout = Qw.QVBoxLayout()
        self.main_layout.addLayout(self.detail_layout)
        self.buttonlayout = Qw.QHBoxLayout()
        self.main_layout.addLayout(self.buttonlayout)

    def _create_Buttons(self):
        self.bcancel = Qw.QPushButton(u'Cancel', self)
        self.bsave = Qw.QPushButton(u'Save', self)
        # Make them loose focus
        self.bcancel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bsave.setFocusPolicy(Qc.Qt.NoFocus)
        # Add them to buttonlayout
        self.buttonlayout.addWidget(self.bcancel)
        self.buttonlayout.addWidget(self.bsave)
        # Make connections
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self.save)

    def _create_fields(self):
        lbs = self.master.field_labels()
        self.mwidgets['id'] = TIntegerKey(parent=self)
        self.mwidgets['id'].setVisible(False)
        for i, fld in enumerate(self.master.field_names()):
            self.mwidgets[fld] = wselector(self.master.field_object(fld), self)
            self.fld_layout.insertRow(
                i, Qw.QLabel(lbs[fld]), self.mwidgets[fld])

    def populate(self):
        if not self._id:
            return
        self.vals = self.master.search_by_id(self._id)
        for key in self.mwidgets:
            self.mwidgets[key].set(self.vals[key])

    @property
    def get_data(self):
        data = {}
        for fld in self.widgets:
            data[fld] = self.widgets[fld].get()
        return data

    def save(self):
        data = self.get_data
        validated, errors = self.model.validate(data)
        if not validated:
            Qw.QMessageBox.information(self, "Error", '\n'.join(errors))
            return
        status, lid = self.model.save(data)
        if status:
            if lid:
                msg = 'New record saved with Νο: %s' % lid
            else:
                msg = 'Record Νο: %s updated' % data['id']
                self.val_updated.emit('%s' % data['id'])
            if CONFIRMATIONS:
                Qw.QMessageBox.information(self, "Save", msg)
            self.accept()
        else:
            Qw.QMessageBox.information(self, "Save", lid)
