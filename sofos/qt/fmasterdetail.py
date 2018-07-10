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
        # self.master_layout = Qw.QFormLayout()
        self.master_layout = Qw.QGridLayout()
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
        self._create_master_fields()
        self.tbl = self._init_table()
        self.detail_layout.addWidget(Qw.QLabel("Δοκιμή"))
        self.detail_layout.addWidget(self.tbl)
        self.tbl.setColumnCount(len(self.detail.field_labels()))
        self.tbl.setHorizontalHeaderLabels(self.detail.field_labels().values())

    def _create_master_fields(self):
        print(len(self.master.field_labels()))
        cols = ((len(self.master.field_labels()) - 2) // 8) + 1
        lbs = self.master.field_labels()
        self.mwidgets['id'] = TIntegerKey(parent=self)
        self.mwidgets['id'].setVisible(False)
        for i, fld in enumerate(self.master.field_names()):
            self.mwidgets[fld] = wselector(self.master.field_object(fld), self)
            j = i // cols
            k = i % cols
            label = Qw.QLabel('%s :' % lbs[fld])
            label.setAlignment(
                Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter)
            self.master_layout.addWidget(label, j, (2 * k) + 0)
            self.master_layout.addWidget(self.mwidgets[fld], j, (2 * k) + 1)

    def _new_detail_line(self):
        self.tbl.setRowCount(self.tbl.rowCount() + 1)
        for i, fld in enumerate(self.detail.field_names()):
            print(i, fld)

    def _init_table(self):
        tbl = Qw.QTableWidget(self)
        tbl.verticalHeader().setStretchLastSection(False)
        tbl.verticalHeader().setVisible(False)
        tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        # tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        # tbl.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        # tbl.setSortingEnabled(True)
        tbl.setContextMenuPolicy(Qc.Qt.ActionsContextMenu)
        newAction = Qw.QAction("New", self)
        tbl.addAction(newAction)
        newAction.triggered.connect(self._new_detail_line)
        editAction = Qw.QAction("Edit", self)
        # editAction.triggered.connect(self._edit_record)
        tbl.addAction(editAction)
        deleteAction = Qw.QAction("Delete", self)
        # deleteAction.triggered.connect(self._delete_record)
        tbl.addAction(deleteAction)
        tbl.horizontalHeader().setContextMenuPolicy(Qc.Qt.CustomContextMenu)
        # tbl.horizontalHeader().customContextMenuRequested.connect(self.fmen)
        # tbl.viewport().update()
        return tbl

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
