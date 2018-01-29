'''
qted module
===========
pyqt controls τροποποιημένα να έχουν ομοιόμορφο τρόπο κλήσης
'''
import datetime
import decimal
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
from . import gr


CONFIRMATIONS = True
GRLOCALE = Qc.QLocale(Qc.QLocale.Greek, Qc.QLocale.Greece)
MSG_RESET_DATE = u'Με δεξί κλίκ του ποντικιού μηδενίζει'
MIN_HEIGHT = 30
MAX_HEIGHT = 40
DATE_MAX_WIDTH = 120
SQLITE_DATE_FORMAT = 'yyyy-MM-dd'
GREEK_DATE_FORMAT = 'd/M/yyyy'
WEEKDAYS = ['Δε', 'Τρ', 'Τε', 'Πέ', 'Πα', 'Σά', 'Κυ']
MSG_SELECT_DAYS = 'Επιλέξτε τις Εργάσιμες ημέρες\nΜε δεξί κλικ μηδενίστε'
BLANK, GREEN = range(2)


# My Qt Widgets
class TCheckbox(Qw.QCheckBox):
    """True or False field: 0 for unchecked , 2 for checked"""
    def __init__(self, val=False, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txtVal):
        self.setChecked(int(txtVal)) if txtVal else self.setChecked(False)

    def get(self):
        return self.checkState()


class TDate(Qw.QDateEdit):
    '''Date values for most cases'''
    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setCalendarPopup(True)
        self.setDisplayFormat(GREEK_DATE_FORMAT)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setMaximumWidth(DATE_MAX_WIDTH)
        # self.setMinimumWidth(par.DATE_MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setLocale(GRLOCALE)

    def set(self, iso_date):
        if iso_date:
            if len(iso_date) > 10:
                iso_date = iso_date[:10]
            yyy, mmm, ddd = iso_date.split('-')
            qdate = Qc.QDate()
            qdate.setDate(int(yyy), int(mmm), int(ddd))
            self.setDate(qdate)
        else:
            self.setDate(Qc.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(SQLITE_DATE_FORMAT)


class TDateEmpty(Qw.QToolButton):
    '''Date or empty string values'''
    def __init__(self, val=None, parent=None):
        super().__init__(parent)
        self.setPopupMode(Qw.QToolButton.MenuButtonPopup)
        self.setMenu(Qw.QMenu(self))
        self.cal = Qw.QCalendarWidget()
        self.action = Qw.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menu_calendar)
        self.setSizePolicy(Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Fixed)
        self.setToolTip(MSG_RESET_DATE)
        self.setMinimumHeight(MIN_HEIGHT)
        self.set(val)

    def mousePressEvent(self, event):
        if event.button() == Qc.Qt.RightButton:
            self.setText('')
            self.cal.setSelectedDate(Qc.QDate.currentDate())
        else:
            Qw.QToolButton.mousePressEvent(self, event)

    def menu_calendar(self):
        self.setText(self.cal.selectedDate().toString(GREEK_DATE_FORMAT))
        self.menu().hide()

    def set(self, iso_date):
        if not iso_date:
            return
        if len(iso_date) == 0:
            return
        yyy, mmm, ddd = iso_date.split('-')
        self.setText('%s/%s/%s' % (ddd, mmm, yyy))
        qdt = Qc.QDate()
        qdt.setDate(int(yyy), int(mmm), int(ddd))
        self.cal.setSelectedDate(qdt)

    def get(self):
        if len(self.text()) == 0:
            return ''
        ddd, mmm, yyy = self.text().split('/')
        qdt = Qc.QDate()
        qdt.setDate(int(yyy), int(mmm), int(ddd))
        return '%s' % qdt.toString(SQLITE_DATE_FORMAT)


class TIntegerSpin(Qw.QSpinBox):
    '''Integer values (eg 123)'''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimum(0)
        self.setMaximum(999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)

    def get(self):
        return self.value()

    def set(self, val):
        self.setValue(int(val)) if val else self.setValue(0)


class TNumeric(Qw.QLineEdit):
    '''Text field with numeric chars only.'''
    def __init__(self, val='0', parent=None):
        super().__init__(parent)
        self.set(val)
        rval = Qc.QRegExp('(\d*)([1-9,])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)

    def focusOutEvent(self, ev):
        self.set(self.get())
        Qw.QLineEdit.focusOutEvent(self, ev)

    def set(self, txt):
        self.setText(gr.dec2gr(txt)) if txt else self.setText(gr.dec2gr(0))

    def get(self):
        greek_div = ','
        normal_div = '.'
        tmp = '%s' % self.text()
        tmp = tmp.replace(normal_div, '')
        tmp = tmp.replace(greek_div, normal_div)
        return gr.dec(tmp.strip())


class TNumericSpin(Qw.QDoubleSpinBox):
    '''Numeric (decimal 2 ) values (eg 999,99)'''
    def __init__(self, val=0, parent=None):
        super().__init__(parent)

        self.set(val)

        self.setMinimum(-99999999999)
        self.setMaximum(99999999999)
        self.setAlignment(Qc.Qt.AlignRight |
                          Qc.Qt.AlignTrailing |
                          Qc.Qt.AlignVCenter)
        self.setButtonSymbols(Qw.QAbstractSpinBox.NoButtons)
        # self.setMinimumHeight(par.MIN_HEIGHT)
        self.setSingleStep(0)  # Για να μην αλλάζει η τιμή με τα βελάκια
        self.setGroupSeparatorShown(True)
        self.setLocale(GRLOCALE)

    def get(self):
        return gr.dec(self.value())

    def set(self, val):
        self.setValue(val) if val else self.setValue(0)


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


class TTextLine(Qw.QLineEdit):
    """Text Line Class"""
    def __init__(self, val='', parent=None):
        super().__init__(parent)
        self.set(val)
        self.setMinimumHeight(MIN_HEIGHT)

    def set(self, txt):
        if txt is not None:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')
        self.setCursorPosition(0)

    def get(self):
        tmp = '%s' % self.text()
        return tmp.strip()


class TInteger(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))
        self.setAlignment(Qc.Qt.AlignRight)


class TTextlineNum(TTextLine):
    '''Text field with numeric chars only left aligned.'''
    def __init__(self, val='', parent=None):
        super().__init__(val, parent)
        rval = Qc.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(Qg.QRegExpValidator(rval))


class TYesNoCombo(Qw.QComboBox):
    '''Yes/No Combo'''
    def __init__(self, val=0, noyes=['No', 'Yes'], parent=None):
        super().__init__(parent)
        self.addItem(noyes[0])
        self.addItem(noyes[1])
        self.set(val)

    def get(self):
        return self.currentIndex() != 0

    def set(self, val):
        idx = 0
        if int(val) != 0:
            idx = 1
        self.setCurrentIndex(idx)


class TWeekdays(Qw.QWidget):
    '''Weekdays selection ([1,1,1,1,1,0,0] 7 values 0 or 1, one per weekday)'''
    def __init__(self, val=[1, 1, 1, 1, 1, 0, 0], parent=None):
        '''pin: {'name': xx, 'vals': [1,1,1,1,1,1,1], 'dayNames': []}'''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.parent = parent
        self.setSizePolicy(
            Qw.QSizePolicy(
                Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Expanding))
        self.set(val)
        self.selected = [0, 0]
        self.dayNames = WEEKDAYS
        self.setMinimumSize(Qc.QSize(170, 20))
        self.setMaximumSize(Qc.QSize(170, 20))
        self.setToolTip(MSG_SELECT_DAYS)
        self.setMinimumHeight(MIN_HEIGHT)

    def sizeHint(self):
        return Qc.QSize(170, 20)

    def mousePressEvent(self, event):
        if event.button() == Qc.Qt.LeftButton:
            xOffset = self.width() / 7
            # yOffset = xOffset #self.height()
            if event.x() < xOffset:
                x = 0
            elif event.x() < 2 * xOffset:
                x = 1
            elif event.x() < 3 * xOffset:
                x = 2
            elif event.x() < 4 * xOffset:
                x = 3
            elif event.x() < 5 * xOffset:
                x = 4
            elif event.x() < 6 * xOffset:
                x = 5
            else:
                x = 6
            cell = self.grid[x]
            if cell == BLANK:
                cell = GREEN
            else:
                cell = BLANK
            self.grid[x] = cell
            self.selected = [x, 0]
            self.update()

        elif event.button() == Qc.Qt.RightButton:
            self.reset()

    def paintEvent(self, event=None):
        painter = Qg.QPainter(self)
        painter.setRenderHint(Qg.QPainter.Antialiasing, True)
        xOffset = self.width() / 7
        yOffset = self.height()
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for x in range(7):
            cell = self.grid[x]
            rect = Qc.QRectF(x * xOffset, 0, xOffset,
                             yOffset).adjusted(0.1, 0.1, -0.1, -0.1)
            color = None
            painter.drawRect(rect.adjusted(2, 2, -2, -2))
            if cell == GREEN:
                color = Qc.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qc.Qt.black)
                painter.setBrush(color)
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qc.Qt.black
                painter.restore()
            painter.setPen(Qc.Qt.black)
            painter.drawText(rect.adjusted(4, 3, -3, -3), self.dayNames[x])
            painter.drawRect(rect)

    def get(self, strVal=True):
        if strVal:
            st = '['
            for i in range(7):
                if i == 6:
                    st += '%s]' % self.grid[i]
                else:
                    st += '%s,' % self.grid[i]
            return st
        else:
            return self.grid

    def set(self, darr=[0, 0, 0, 0, 0, 0, 0]):
        # Set values to days vector. But first checks for
        # proper array length and type
        darr = '%s' % darr
        tmparr = eval(darr)
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0, 0, 0, 0, 0, 0, 0]
        self.update()

    def reset(self):
        'Set everything to Null'
        self.set([0, 0, 0, 0, 0, 0, 0])

    def set5days(self):
        'Set Standard five days week'
        self.set([1, 1, 1, 1, 1, 0, 0])


class TCombo(Qw.QComboBox):
    '''Combo'''
    def __init__(self, val=0, vlist=[], parent=None):
        super().__init__(parent)
        self.populate(vlist)
        self.set(val)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[id_])

    def populate(self, vlist):
        """
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        self.index2id = {}
        self.id2index = {}
        for i, elm in enumerate(vlist):
            self.addItem('%s' % elm[1])
            self.index2id[i] = elm[0]
            self.id2index[elm[0]] = i


class TComboDB(Qw.QComboBox):
    '''Combo'''
    def __init__(self, idv, model, parent):
        super().__init__(parent)
        self._parent = parent
        self._model = model
        self.populate()
        self.set(idv)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[int(id_)])

    def populate(self):
        """
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        vlist = self._model.select_all(self._parent._dbf)
        self.index2id = {}
        self.id2index = {}
        self.addItem('')
        self.index2id[0] = ''
        self.id2index[''] = 0
        for i, elm in enumerate(vlist['rows']):
            self.addItem('%s' % elm[1])
            self.index2id[i+1] = elm[0]
            self.id2index[elm[0]] = i+1


class AutoForm(Qw.QDialog):
    def __init__(self, dbf, model, idv=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self._parent = parent
        self._dbf = dbf
        self._id = idv
        self.model = model
        self.setWindowTitle('{}: {}'.format(model.table_label(),
                                            idv if idv else 'Νέα εγγραφή'))
        self.widgets = {}
        main_layout = Qw.QVBoxLayout()
        self.setLayout(main_layout)
        self.fld_layout = Qw.QFormLayout()
        main_layout.addLayout(self.fld_layout)
        # Create buttons
        buttonlayout = Qw.QHBoxLayout()
        main_layout.addLayout(buttonlayout)
        # Create buttons here
        self.bcancel = Qw.QPushButton(u'Ακύρωση', self)
        self.bsave = Qw.QPushButton(u'Αποθήκευση', self)
        # Make them loose focus
        self.bcancel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bsave.setFocusPolicy(Qc.Qt.NoFocus)
        # Add them to buttonlayout
        buttonlayout.addWidget(self.bcancel)
        buttonlayout.addWidget(self.bsave)
        # Make connections here
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self._save)
        self._create_fields()  # Δημιουργία widgets
        if self._id:  # Γέμισμα με τιμές
            self._fill()

    def _create_fields(self):
        lbs = self.model.field_labels()
        self.widgets['id'] = TInteger(parent=self)
        self.widgets['id'].setVisible(False)
        for i, fld in enumerate(self.model.fields()):
            self.widgets[fld] = wselector(self.model.field(fld), self)
            self.fld_layout.insertRow(i, Qw.QLabel(lbs[fld]),
                                      self.widgets[fld])

    def _fill(self):
        self.vals = self.model.search_by_id(self._dbf, self._id)
        for key in self.vals:
            self.widgets[key].set(self.vals[key])

    def _save(self):
        data = {}
        for fld in self.widgets:
            data[fld] = self.widgets[fld].get()
        status, lid = self.model.save_meta(self._dbf, data)
        if status:
            if lid:
                msg = 'Νέα εγγραφή καταχωρήθηκε με Νο: %s' % lid
            else:
                msg = 'Ενημερώθηκε η εγγραφή Νο: %s' % data['id']
            if CONFIRMATIONS:
                Qw.QMessageBox.information(self, "Αποθήκευση", msg)
            self.accept()
        else:
            Qw.QMessageBox.information(self, "Αποθήκευση", lid)

    def userFriendlyCurrentFile(self):
        return self.table


class FindForm(AutoForm):
    def __init__(self, dbf, table, parent=None):
        super().__init__(dbf, table, parent=parent)
        self.bsave.setText('Αναζήτηση')
        self.bsave.setFocusPolicy(Qc.Qt.StrongFocus)

    def _save(self):
        ast = []
        for fld in self.widgets:
            wval = self.widgets[fld].get()
            if wval:
                ast.append(wval)
        ast = ' '.join(ast)
        formgrid = AutoFormTableFound(self._dbf, self._table, ast, self)
        if formgrid.exec_() == Qw.QDialog.Accepted:
            print(formgrid.id)


class AutoFormTable(Qw.QDialog):
    def __init__(self, dbf, model, parent=None):
        super().__init__(parent)
        # self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.resize(550, 400)
        self._parent = parent
        self._dbf = dbf
        self.model = model  # md.Model(dbf, table)
        self.setWindowTitle('{}'.format(self.model.table_label()))
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        self.tbl = self._init_table()
        layout.addWidget(self.tbl)
        blay = Qw.QHBoxLayout()
        layout.addLayout(blay)
        self.bedt = Qw.QPushButton('Επεξεργασία')
        self.bedt.setFocusPolicy(Qc.Qt.NoFocus)
        blay.addWidget(self.bedt)
        self.bnew = Qw.QPushButton('Νέα εγγραφή')
        self.bnew.setFocusPolicy(Qc.Qt.NoFocus)
        blay.addWidget(self.bnew)
        self.bedt.clicked.connect(self._edit_record)
        self.bnew.clicked.connect(self._new_record)
        self.tbl.cellDoubleClicked.connect(self._edit_record)
        self._populate()

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection'''
        if ev.key() in (Qc.Qt.Key_Enter, Qc.Qt.Key_Return):
            self._edit_record()
        elif ev.key() == Qc.Qt.Key_Insert:
            self._new_record()
        Qw.QDialog.keyPressEvent(self, ev)

    def _new_record(self):
        dialog = AutoForm(self._dbf, self.model, parent=self)
        if dialog.exec_() == Qw.QDialog.Accepted:
            self._populate()
        else:
            return False

    @property
    def id(self):
        return self.tbl.item(self.tbl.currentRow(), 0).text()

    def _edit_record(self):
        dialog = AutoForm(self._dbf, self.model, self.id, parent=self)
        if dialog.exec_() == Qw.QDialog.Accepted:
            self._populate()
        else:
            return False

    def _get_data(self):
        return self.model.select_all(self._dbf)

    def _populate(self):
        data = self._get_data()
        self.tbl.setRowCount(data['rownum'])
        self.tbl.setColumnCount(data['colnum'])
        dlbl = self.model.field_labels()
        labels = [dlbl[i] for i in data['cols']]
        self.tbl.setHorizontalHeaderLabels(labels)
        for i, row in enumerate(data['rows']):
            for j, col in enumerate(data['cols']):
                val = row[j]
                field = data['cols'][j]
                if field.startswith('id'):
                    item = self._intItem(val)
                # elif data['cols'][j].endswith('_id'):
                #     item = self._keyItem(val, data['cols'][j][:-3])
                # elif data['cols'][j].endswith('_cd'):
                #     item = self._keyItem(val, data['cols'][j][:-3])
                elif self.model.field(field).typos == 'INTEGER':
                    item = self._intItem(val)
                elif self.model.field(field).typos == 'DECIMAL':
                    item = self._numItem(val)
                elif self.model.field(field).typos == 'DATE':
                    item = SortWidgetItem(gr.date2gr(val), val)
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
        editAction = Qw.QAction("Επεξεργασία", self)
        editAction.triggered.connect(self._edit_record)
        tbl.addAction(editAction)
        return tbl

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

    def _keyItem(self, strv, table):
        stv = md.table_rpr(self._dbf, table, strv)
        if stv == 'None':
            stv = ''
        item = Qw.QTableWidgetItem(stv)
        return item

    def table_label(self):
        return self.model.table_label()


class AutoFormTableFound(AutoFormTable):
    def __init__(self, dbf, model, search_string, parent=None):
        print('asdfsadfsdf sadfsadf')
        self.search_string = search_string
        super().__init__(dbf, model, parent)
        self.tbl.cellDoubleClicked.disconnect(self._edit_record)
        self.tbl.cellDoubleClicked.connect(self.accept)

    def _get_data(self):
        return self.model.search(self._dbf, self.search_string)

    def keyPressEvent(self, ev):
        '''use enter or return for fast selection'''
        if ev.key() in (Qc.Qt.Key_Enter, Qc.Qt.Key_Return):
            self.accept()
        Qw.QDialog.keyPressEvent(self, ev)


class SortWidgetItem(Qw.QTableWidgetItem):
    """Sorting"""
    def __init__(self, text, sortKey):
        super().__init__(text, Qw.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


class TTextButton(Qw.QWidget):
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, idv, model, parent):
        """parent must have ._dbf"""
        super().__init__(parent)
        self._parent = parent
        self._dbf = parent._dbf
        self._model = model
        self.txt_initial = ''
        # Create Gui
        self._create_gui()
        if idv:
            self.set(idv)

    def set(self, idv):
        if idv is None or idv == 'None':
            return
        dicval = self._model.search_by_id(self._dbf, idv)
        self._set_state(1 if dicval else 0)
        self.txt_initial = self._rpr(dicval)
        self.rpr = self.txt_initial
        self.text.setText(self.txt_initial)
        self.setToolTip(self.txt_initial)
        self.text.setCursorPosition(0)
        self.idv = dicval['id']

    def _rpr(self, dicval):
        ltxt = []
        for key in dicval:
            if key != 'id':
                ltxt.append(str(dicval[key]))
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

    def _set_state(self, state):
        self._state = state
        sred = 'background-color: rgba(239, 41, 41);'
        sgreen = 'background-color: rgba(0, 180, 0);'
        self.button.setStyleSheet(sred if state == 0 else sgreen)

    def _text_changed(self):
        self._set_state(0 if self.txt_initial != self.text.text() else 1)

    def _button_clicked(self):
        self.button.setFocus()
        # vals = self._model.select_all(self._dbf)
        ffind = AutoFormTableFound(self._parent._dbf, self._model, '', self)
        if ffind.exec_() == Qw.QDialog.Accepted:
            self.set(ffind.id)
        else:
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
        vals = self._model.search(self._dbf, text)
        if vals['rownum'] == 1:
            self.set(vals['rows'][0][0])
        elif vals['rownum'] > 1:
            ffind = AutoFormTableFound(self._parent._dbf, self._table,
                                       text, self)
            if ffind.exec_() == Qw.QDialog.Accepted:
                self.set(ffind.id)
            else:
                self._set_state(1 if self.txt == self.text.text() else 0)
        else:
            self.valNotFound.emit(self.text.text())



    def get(self):
        return self.idv


def wselector(field, parent):
    if field.qt_widget == 'int':
        return TInteger(parent=parent)
    elif field.qt_widget == 'text_button':
        return TTextButton(None, field.ftable, parent)
    elif field.qt_widget == 'combo':
        return TComboDB(None, field.ftable, parent)
    elif field.qt_widget == 'check_box':
        return TCheckbox(parent=parent)
    elif field.qt_widget == 'date':
        return TDate(parent=parent)
    elif field.qt_widget == 'date_or_empty':
        return TDateEmpty(parent=parent)
    elif field.qt_widget == 'num':
        return TNumeric(parent=parent)
    elif field.qt_widget == 'text_num':
        return TTextlineNum(parent=parent)
    elif field.qt_widget == 'text':
        return TText(parent=parent)
    elif field.qt_widget == 'week_days':
        return TWeekdays(parent=parent)
    elif field.qt_widget == 'str':
        return TTextLine(parent=parent)
    else:
        return TTextLine(parent=parent)
