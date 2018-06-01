import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .. import gr
from .fautoform import AutoForm
from .settings import WEEKDAYS_FULL
from .vsortwidgetitem import SortWidgetItem


class AutoFormTable(Qw.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        # self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.settings = Qc.QSettings()
        self._fld_action = {}
        self.model = model
        self._wtitle()
        self._create_gui()
        self._make_connections()
        self._populate()
        self._hide_cols()

    def closeEvent(self, event):
        keyv = "Forms/%ssiz" % self.model.table_name()
        self.settings.setValue(keyv, self.size())

    def _wtitle(self):
        self.setWindowTitle('{}'.format(self.model.table_label()))

    def _make_connections(self):
        self.bedit.clicked.connect(self._edit_record)
        self.bnew.clicked.connect(self._new_record)
        self.tbl.cellDoubleClicked.connect(self._edit_record)

    def _create_gui(self):
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        self.tbl = self._init_table()
        layout.addWidget(self.tbl)
        blay = Qw.QHBoxLayout()
        layout.addLayout(blay)
        self.bedit = Qw.QPushButton('Edit')
        self.bedit.setFocusPolicy(Qc.Qt.NoFocus)
        blay.addWidget(self.bedit)
        self.bnew = Qw.QPushButton('New record')
        self.bnew.setFocusPolicy(Qc.Qt.NoFocus)
        blay.addWidget(self.bnew)

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection'''
        if ev.key() in (Qc.Qt.Key_Enter, Qc.Qt.Key_Return):
            self._edit_record()
        elif ev.key() == Qc.Qt.Key_Insert:
            self._new_record()
        # Qw.QDialog.keyPressEvent(self, ev)

    def _new_record(self):
        dialog = AutoForm(self.model, parent=self)
        if dialog.exec_() == Qw.QDialog.Accepted:
            self._populate()
        else:
            return False

    @property
    def id(self):
        return self.tbl.item(self.tbl.currentRow(), 0).text()

    def _edit_record(self):
        if not hasattr(self, 'id'):
            return False
        dialog = AutoForm(self.model, self.id, parent=self)
        main_window = self.parent().parent().parent().parent()
        if hasattr(main_window, 'refresh_forms'):
            dialog.val_updated.connect(main_window.refresh_forms)
        if dialog.exec_() == Qw.QDialog.Accepted:
            self._populate()
        else:
            return False

    def _get_data(self):
        return self.model.select_ful_deep()

    def _populate(self):
        data = self._get_data()
        self.tbl.setRowCount(data['rownum'])
        self.tbl.setColumnCount(data['colnum'])
        self.tbl.setHorizontalHeaderLabels(data['labels'])
        for i, row in enumerate(data['rows']):
            for j, qt_widget in enumerate(data['qt_widgets_types']):
                val = row[j]
                if qt_widget == 'int':
                    item = self._intItem(val)
                elif qt_widget == 'num':
                    item = self._numItem(val)
                elif qt_widget == 'date':
                    item = SortWidgetItem(gr.date2gr(val), val)
                elif qt_widget == 'week_days':
                    item = self._weekdayItem(val)
                else:
                    item = self._strItem(val)
                self.tbl.setItem(i, j, item)
        self.tbl.resizeColumnsToContents()

    def _init_table(self):
        tbl = Qw.QTableWidget(self)
        tbl.verticalHeader().setStretchLastSection(False)
        tbl.verticalHeader().setVisible(False)
        tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        tbl.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setSortingEnabled(True)
        tbl.setContextMenuPolicy(Qc.Qt.ActionsContextMenu)
        editAction = Qw.QAction("Edit", self)
        editAction.triggered.connect(self._edit_record)
        tbl.addAction(editAction)
        deleteAction = Qw.QAction("Delete", self)
        deleteAction.triggered.connect(self._delete_record)
        tbl.addAction(deleteAction)
        tbl.horizontalHeader().setContextMenuPolicy(Qc.Qt.ActionsContextMenu)
        vfd = self.model.sql_select_ful_deep()
        lbls, cols = vfd['labels'], vfd['cols']
        keyv = "Forms/%s" % self.model.table_name()
        keyvset = self.settings.value(keyv, defaultValue=None)
        for i, col in enumerate(cols):
            self._fld_action[col] = Qw.QAction(lbls[i], self)
            self._fld_action[col].setCheckable(True)
            if keyvset:
                bval = keyvset.get(col, True)
            else:
                bval = True
            self._fld_action[col].setChecked(bval)
            self._fld_action[col].triggered.connect(self._toggle_flds)
            tbl.horizontalHeader().addAction(self._fld_action[col])
        tbl.viewport().update()
        return tbl

    def _hide_cols(self):
        for i, fldaction in enumerate(self._fld_action.keys()):
            if self._fld_action[fldaction].isChecked():
                self.tbl.setColumnHidden(i, False)
            else:
                self.tbl.setColumnHidden(i, True)
        self.tbl.resizeColumnsToContents()

    def _toggle_flds(self):
        vls = {}
        for i, fldaction in enumerate(self._fld_action.keys()):
            if self._fld_action[fldaction].isChecked():
                self.tbl.setColumnHidden(i, False)
                vls[fldaction] = True
            else:
                self.tbl.setColumnHidden(i, True)
                vls[fldaction] = False
        # print(self.model.table_name(), vls)
        keyv = "Forms/%s" % self.model.table_name()
        self.settings.setValue(keyv, vls)
        # aaa = self.settings.value(keyv, defaultValue=None)
        # print(aaa)
        self.tbl.resizeColumnsToContents()

    def _delete_record(self):
        """Delete Record"""
        success, msg = self.model.delete(self.id)
        if success:
            self._populate()
        else:
            Qw.QMessageBox.critical(self, "Delete Error", msg)

    def _intItem(self, num):
        item = Qw.QTableWidgetItem()
        item.setData(Qc.Qt.DisplayRole, num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _numItem(self, num):
        item = SortWidgetItem(gr.dec2gr(num), num)
        item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        return item

    def _strItem(self, strv):
        st = str(strv)
        if st == 'None':
            st = ''
        item = Qw.QTableWidgetItem(st)
        return item

    def _weekdayItem(self, strv):
        weekdays_list = eval(strv)
        weekdays_string_list = []
        for i, wday in enumerate(weekdays_list):
            if wday != 0:
                weekdays_string_list.append(WEEKDAYS_FULL[i])
        item = Qw.QTableWidgetItem(', '.join(weekdays_string_list))
        return item

    def table_label(self):
        return self.model.table_label()
