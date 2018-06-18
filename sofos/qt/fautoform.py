import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .ttextline import TIntegerKey
from .widget_selector import wselector
from .settings import CONFIRMATIONS


class AutoForm(Qw.QDialog):
    val_updated = Qc.pyqtSignal(str)

    def __init__(self, model, idv=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.locked = False
        self._set(model, idv)
        self._wtitle()
        self._create_layouts()
        self._create_Buttons()
        self._create_fields()
        self.populate()

    def _wtitle(self):
        self.setWindowTitle('{}: {}'.format(
            self.model.table_label(), self._id if self._id else 'New record'))

    def _set(self, model, idv):
        self._id = idv
        self.model = model
        self.widgets = {}

    def _create_layouts(self):
        self.main_layout = Qw.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.fld_layout = Qw.QFormLayout()
        self.main_layout.addLayout(self.fld_layout)
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
        self.bsave.clicked.connect(self.btnsave)

    def _create_fields(self):
        lbs = self.model.field_labels()
        self.widgets['id'] = TIntegerKey(parent=self)
        self.widgets['id'].setVisible(False)
        for i, fld in enumerate(self.model.field_names()):
            # self.widgets[fld] = wselector(self.model.field_object(fld), self)
            self.widgets[fld] = self.model.field_object(fld).qwl(self)
            self.fld_layout.insertRow(
                i, Qw.QLabel(lbs[fld]), self.widgets[fld])

    def populate(self):
        if not self._id:
            return
        self.vals = self.model.search_by_id(self._id)
        for key in self.widgets:
            self.widgets[key].set(self.vals[key])
        self.lock()

    @property
    def get_data(self):
        data = {}
        for fld in self.widgets:
            data[fld] = self.widgets[fld].get()
        return data

    def lock(self):
        for widget in self.widgets.values():
            widget.setEnabled(False)
        self.bsave.setText('Edit')
        self.locked = True

    def unlock(self):
        for widget in self.widgets.values():
            widget.setEnabled(True)
        self.bsave.setText('Save')
        self.locked = False

    def btnsave(self):
        if self.locked:
            self.unlock()
        else:
            self.save()

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
