import PyQt5.QtWidgets as Qw


class TText(Qw.QTextEdit):
    """Text field"""
    def __init__(self, val='', parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        # self.setMinimumHeight(60)
        self.set(val)

    def set(self, txt):
        """:param txt: value to set"""
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')

    def get(self):
        """:return: Text value of control"""
        tmpval = '%s' % self.toPlainText().replace("'", "''")
        return tmpval.strip()
