import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .. import gr
from .fautoform import AutoForm
from .settings import WEEKDAYS_FULL
from .vsortwidgetitem import SortWidgetItem


class FieldsToView(Qw.QDialog):
    def __init__(self, fldList, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Visible Fields')
        layout = Qw.QVBoxLayout(self)
        scroll = Qw.QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        scont = Qw.QWidget()
        vlay = Qw.QVBoxLayout(scont)
        vlay.setAlignment(Qc.Qt.AlignTop)
        scroll.setWidget(scont)
        self.fields = fldList
        self.fld_widgets = {}
        for elm in fldList:
            self.fld_widgets[elm[0]] = Qw.QCheckBox(elm[1])
            self.fld_widgets[elm[0]].setChecked(elm[2])
            vlay.addWidget(self.fld_widgets[elm[0]])
        btnlay = Qw.QHBoxLayout()
        layout.addLayout(btnlay)
        btn = Qw.QPushButton('ok')
        bde = Qw.QPushButton('cancel')
        btnlay.addWidget(bde)
        btnlay.addWidget(btn)
        bde.setFocusPolicy(Qc.Qt.NoFocus)
        btn.clicked.connect(self.hide_columns)
        bde.clicked.connect(self.cancel)

    def are_all_hidden(self):
        total_widgets = len(self.fld_widgets)
        total_hidden = 0
        for elm in self.fld_widgets:
            if not self.fld_widgets[elm].isChecked():
                total_hidden += 1
        return total_widgets == total_hidden

    def update_sdict(self):
        for elm in self.fld_widgets:
            self.parent().sdict[elm] = self.fld_widgets[elm].isChecked()

    def hide_columns(self):
        if self.are_all_hidden():
            Qw.QMessageBox.critical(
                self, 'Error', 'Set at least one visible column ')
            return
        self.update_sdict()
        self.parent().hide_cols()
        self.parent().save_settings()
        self.accept()

    def cancel(self):
        self.accept()


class AutoFormTable(Qw.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        # self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.settings = Qc.QSettings()
        self._fld_action = {}
        self._fld_visible = {}
        self.model = model
        self.sname = "VisibleFields/%s" % self.model.table_name()
        self.sdict = self.settings.value(self.sname, defaultValue={})
        self._wtitle()
        self._create_gui()
        self._make_connections()
        self._populate()
        self.hide_cols()

    def closeEvent(self, event):
        keyv = "FormSize/%s" % self.model.table_name()
        size = self.size()
        xvl = self.geometry().x()
        yvl = self.geometry().y()
        size.setWidth(size.width() + xvl + xvl)
        size.setHeight(size.height() + xvl + yvl)
        self.settings.setValue(keyv, size)

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
        return self.model.select_all_deep()

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
                elif qt_widget == 'date_or_empty':
                    if len(str(val)) > 0:
                        item = SortWidgetItem(gr.date2gr(val), val)
                    else:
                        item = self._strItem(val)
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
        tbl.horizontalHeader().setContextMenuPolicy(Qc.Qt.CustomContextMenu)
        tbl.horizontalHeader().customContextMenuRequested.connect(self.fmen)
        # tbl.viewport().update()
        return tbl

    def fmen(self, position):
        vfd = self.model.sql_select_all_deep()
        lbls, cols = vfd['labels'], vfd['cols']
        data = []
        for i, col in enumerate(cols):
            data.append([col, lbls[i], self.sdict.get(col, True)])
        frm = FieldsToView(data, self)
        frm.move(self.mapToGlobal(position))
        frm.exec_()

    def hide_cols(self):
        vfd = self.model.sql_select_all_deep()
        cols = vfd['cols']
        for i, col in enumerate(cols):
            self.tbl.setColumnHidden(i, not self.sdict.get(col, True))
        self.tbl.resizeColumnsToContents()

    def save_settings(self):
        self.settings.setValue(self.sname, self.sdict)

    def _delete_record(self):
        """Delete Record"""
        success, msg = self.model.delete(self.id)
        if success:
            self._populate()
        else:
            Qw.QMessageBox.critical(self, "Not allowed to delete", msg)

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
        weekdays_list = eval(strv.replace('!', "'"))
        items = []
        for i, wday in enumerate(weekdays_list):
            if wday != '':
                items.append('%s(%s)' % (WEEKDAYS_FULL[i], wday))
        return Qw.QTableWidgetItem(', '.join(items))

    def table_label(self):
        return self.model.table_label()
