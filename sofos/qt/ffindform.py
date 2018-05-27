import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .fautoform import AutoForm


class FindForm(AutoForm):
    """Use this form to search each fields values"""
    def __init__(self, model, parent=None):
        super().__init__(model, parent=parent)
        self.bsave.setText('Search')
        self.bsave.setFocusPolicy(Qc.Qt.StrongFocus)

    def _save(self):
        ast = []
        for fld in self.widgets:
            wval = self.widgets[fld].get()
            if wval:
                ast.append(wval)
        ast = ' '.join(ast)
        formgrid = AutoFormTableFound(self._table, ast, self)
        if formgrid.exec_() == Qw.QDialog.Accepted:
            print(formgrid.id)
