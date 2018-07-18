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
        self._new_detail_line()

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
        # if number of fields is more than 8 create another column fo fields
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
        row = self.tbl.rowCount()
        self.tbl.setRowCount(row + 1)
        dwidgets = {'id': TIntegerKey(parent=self)}
        self.tbl.setCellWidget(row, 0, dwidgets['id'])
        for i, fld in enumerate(self.detail.field_names()):
            dwidgets[fld] = wselector(self.detail.field_object(fld), self)
            self.tbl.setCellWidget(row, i + 1,  dwidgets[fld])
            if fld == self.key:
                self.tbl.hideColumn(i + 1)
        self.dwidgets.append(dwidgets)
        self.tbl.hideColumn(0)

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

    def get_data(self):
        data = {}
        for fld in self.mwidgets:
            data[fld] = self.mwidgets[fld].get()
        data['z'] = []
        for i, line in enumerate(self.dwidgets):
            data['z'].append({})
            for fld in line:
                data['z'][i][fld] = line[fld].get()
        print(data)
        return data

    def save(self):
        data = self.get_data()
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
