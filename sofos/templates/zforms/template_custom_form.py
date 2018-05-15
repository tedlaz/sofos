"""Template form"""
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
# import PyQt5.QtGui as Qg
NAME = 'test1'
MENU = 'Custom Forms'
TITLE = 'Template custom form'


class UForm(Qw.QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.model = model
        self.setWindowTitle(TITLE)
        self.create_ui()

    def table_label(self):
        return TITLE

    def create_ui(self):
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        txtv = Qw.QTextEdit(self)
        layout.addWidget(txtv)
        txtv.setText('%s' % self.model.table_objects())