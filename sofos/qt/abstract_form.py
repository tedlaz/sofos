import json
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from sofos.qt import widget_selector as ws


class AbstractForm(Qw.QDialog):
    def __init__(self, model, idv=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        main_layout = Qw.QVBoxLayout(self)
        self.fld_layout = Qw.QFormLayout()
        main_layout.addLayout(self.fld_layout)
        self.button_layout = Qw.QHBoxLayout()
        main_layout.addLayout(self.button_layout)
        self.add_buttons()
        self.model = model
        self.idv = idv or ''
        self.widgets = {}
        self.create_gui()

    def add_buttons(self):
        self.bcancel = Qw.QPushButton(u'Cancel', self)
        self.bsave = Qw.QPushButton(u'Save', self)
        # Make them loose focus
        self.bcancel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bsave.setFocusPolicy(Qc.Qt.NoFocus)
        # Add them to buttonlayout
        self.button_layout.addWidget(self.bcancel)
        self.button_layout.addWidget(self.bsave)
        # Make connections
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self.save)

    def create_gui(self):
        raise NotImplementedError

    def set_data(self):
        pass

    def add_widget(self, fld_name, title, widget='str'):
        self.widgets[fld_name] = ws.widget_by_name(widget, self)
        no = len(self.widgets)
        self.fld_layout.insertRow(no, Qw.QLabel(title), self.widgets[fld_name])

    def get_data(self, typ=None):
        data = {'id': self.idv}
        for fld in self.widgets:
            data[fld] = self.widgets[fld].get()
        fdi = {'table': self.model, 'data': data}
        if typ == 'json':
            return json.dumps(fdi, ensure_ascii=False)
        return fdi

    def close(self):
        self.accept()

    def save(self):
        print(self.get_data())


class Test(AbstractForm):
    def __init__(self):
        super().__init__('tbl1', None, None)
        self.setWindowTitle('This is a test')

    def create_gui(self):
        self.add_widget('malakia', 'Μαλακία')
        self.add_widget('dokimi', 'Πρόγραμμα', 'week_days')
        self.add_widget('dat', 'Δοκιμή', 'date_or_empty')
        self.add_widget('rrt', 'sfdsf', 'date')
        dff = {'table-master': 'erg',
               'table-detail': 'ergd',
               'key': 'erg',
               'delete-master-id': 13,
               'save-master': {'id': '', 'epo': 'Lazaros'},
               'save-detail': [{'id': '', 'r1': 'vl1'},
                               {'id': '', 'r1': 'vl2'}],
               'delete-detail-ids': [12, 15]
               }


if __name__ == '__main__':
    import sys
    app = Qw.QApplication(sys.argv)
    mainWin = Test()
    mainWin.show()
    sys.exit(app.exec_())
