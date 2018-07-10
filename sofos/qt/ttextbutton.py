import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc


class TTextButton(Qw.QWidget):
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, idv, model, parent):
        """parent must have ._dbf"""
        super().__init__(parent)
        self._parent = parent
        self._model = model
        self.txt_initial = ''
        # Create Gui
        self._create_gui()
        self.set(idv)

    def set(self, idv):
        # if no Value in idv just return
        if idv is None or idv == 'None' or idv == '':
            self.idv = ''
            self._set_state(0)
            return
        dicval = self._model.search_by_id_deep(idv)
        self._set_state(1 if dicval else 0)
        self.txt_initial = self._rpr(dicval)
        self.rpr = self.txt_initial
        self.text.setText(self.txt_initial)
        # self.setToolTip(self.txt_initial)
        fld_list = ['%s:%s' % (i, j) for i, j in dicval.items()]
        self.setToolTip('\n'.join(fld_list))
        self.text.setCursorPosition(0)
        self.idv = dicval['id']

    def tooltip(self):
        flds = self._model.deep_fields()
        lbls = self._model.deep_labels()

    def _rpr(self, dicval):
        # print('line 40:', self._model.repr_fields(), dicval)
        ltxt = [str(dicval[key]) for key in self._model.repr_fields()]
        return ' '.join(ltxt)

    def _create_gui(self):
        self.text = Qw.QLineEdit(self)
        self.button = Qw.QToolButton(self)
        self.button.setArrowType(Qc.Qt.DownArrow)
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        layout = Qw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        # Connections
        self.text.textChanged.connect(self._text_changed)
        self.button.clicked.connect(self._button_clicked)
        # self.button.clicked.connect(self._edit_record)

    def _set_state(self, state):
        self._state = state
        bred = 'background-color: rgba(243, 206, 206);'
        bgreen = 'background-color: rgba(227, 253, 219);'
        # sred = 'color: rgba(239, 41, 41);'
        # sgreen = 'color: rgba(0, 180, 0);'
        # self.button.setStyleSheet(sred if state == 0 else sgreen)
        self.text.setStyleSheet(bred if state == 0 else bgreen)

    def _text_changed(self):
        self._set_state(0 if self.txt_initial != self.text.text() else 1)

    def _button_clicked(self):
        from .fautoformtablefound import AutoFormTableFound
        self.button.setFocus()
        # vals = self._model.select_all(self._dbf)
        ffind = AutoFormTableFound(self._model, '', self)
        if ffind.exec_() == Qw.QDialog.Accepted:
            self.set(ffind.id)
        else:
            if not self.text.text():
                return
            self._set_state(1 if self.txt_initial == self.text.text() else 0)

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.txt_initial != self.text.text():
                self._find(self.text.text())
        return Qw.QWidget.keyPressEvent(self, ev)

    def _find(self, text):
        """
        :param text: text separated by space multi-search values 'va1 val2 ..'
        """
        from .fautoformtablefound import AutoFormTableFound
        vals = self._model.search_deep(text)
        if vals['rownum'] == 1:
            self.set(vals['rows'][0][0])  # Assuming first val is id
        elif vals['rownum'] > 1:
            ffind = AutoFormTableFound(self._model, text, self)
            if ffind.exec_() == Qw.QDialog.Accepted:
                self.set(ffind.id)
        else:
            self.valNotFound.emit(self.text.text())

    def get(self):
        return self.idv

    def _edit_record(self):
        from .fautoform import AutoForm
        dialog = AutoForm(self._model, self.idv, parent=self)
        main_window = self.parent().parent().parent().parent()
        if hasattr(main_window, 'refresh_forms'):
            dialog.val_updated.connect(main_window.refresh_forms)
        if dialog.exec_() == Qw.QDialog.Accepted:
            pass
            # self._populate()
        else:
            return False
