import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
WEEKDAYS = ['ΔΕΥΤΕΡΑ', 'ΤΡΙΤΗ', 'ΤΕΤΑΡΤΗ', 'ΠΕΜΠΤΗ',
            'ΠΑΡΑΣΚΕΥΗ', 'ΣΑΒΒΑΤΟ', 'ΚΥΡΙΑΚΗ']
WIDTH = 500
HEIGH = 50
COLORON = Qg.QColor(100, 255, 100)


def calc_hours(time_range):
    """timer : '23:45-02:05'"""
    assert time_range[2] == ':'
    assert time_range[5] == '-'
    assert time_range[8] == ':'
    apo, eos = time_range.split('-')
    apoh, apom = apo.split(':')
    eosh, eosm = eos.split(':')
    apohi = int(apoh)
    apomi = int(apom)
    eoshi = int(eosh)
    eosmi = int(eosm)
    if eosmi < apomi:
        eosmi += 60
        eoshi -= 1
    if eoshi < apohi:
        eoshi += 24
    mdif = eosmi - apomi
    hdif = eoshi - apohi
    # print('{:02d}:{:02d}'.format(hdif, mdif))
    decimal_timedif = '{:.2f}'.format(hdif + mdif / 60)
    return float(decimal_timedif)


def calc_multiple_hours(time_string):
    """time_string: '10:20-12:20|15:30-18:30' """
    total_time = 0
    if '|' in time_string:
        values = time_string.split('|')
        for val in values:
            total_time += calc_hours(val)
    else:
        total_time = calc_hours(time_string)
    return total_time


class DayHours(Qw.QDialog):
    def __init__(self, day, vals, parent):
        super().__init__(parent)
        """vals: str"""
        self.setWindowTitle(day)
        self.day = day
        self.vals = vals
        malay = Qw.QVBoxLayout(self)
        flayout = Qw.QFormLayout()
        malay.addLayout(flayout)
        blayout = Qw.QHBoxLayout()
        malay.addLayout(blayout)
        self.bcancel = Qw.QPushButton('Cancel')
        self.bcancel.clicked.connect(self.bcancel_pr)
        self.bsave = Qw.QPushButton('Set')
        self.bsave.clicked.connect(self.bsave_pr)
        blayout.addWidget(self.bcancel)
        blayout.addWidget(self.bsave)
        self.apo = Qw.QTimeEdit()
        self.apo.setDisplayFormat('hh:mm')
        self.eos = Qw.QTimeEdit()
        self.eos.setDisplayFormat('hh:mm')
        flayout.insertRow(0, Qw.QLabel('Από'), self.apo)
        flayout.insertRow(1, Qw.QLabel('Έως'), self.eos)
        self.apo2 = Qw.QTimeEdit()
        self.apo2.setDisplayFormat('hh:mm')
        self.eos2 = Qw.QTimeEdit()
        self.eos2.setDisplayFormat('hh:mm')
        flayout.insertRow(2, Qw.QLabel('Από(2)'), self.apo2)
        flayout.insertRow(3, Qw.QLabel('Έως(2)'), self.eos2)
        self.split_values()

    def split_values(self):
        vls = self.vals.split('|')
        if vls[0] == '':
            apoh = apom = eosh = eosm = 0
        else:
            apo, eos = vls[0].split('-')
            apoh, apom = apo.split(':')
            eosh, eosm = eos.split(':')
        self.apo.setTime(Qc.QTime(int(apoh), int(apom)))
        self.eos.setTime(Qc.QTime(int(eosh), int(eosm)))
        if len(vls) == 1:
            return
        if vls[1] == '':
            apoh = apom = eosh = eosm = 0
        else:
            apo, eos = vls[1].split('-')
            apoh, apom = apo.split(':')
            eosh, eosm = eos.split(':')
        self.apo2.setTime(Qc.QTime(int(apoh), int(apom)))
        self.eos2.setTime(Qc.QTime(int(eosh), int(eosm)))

    def get_vals(self):
        val = '%s-%s' % (self.apo.text(), self.eos.text())
        if val == "00:00-00:00":
            val = ""
        val2 = '%s-%s' % (self.apo2.text(), self.eos2.text())
        if val2 == "00:00-00:00":
            val2 = ""
        if val == "" or val2 == "":
            return val
        return '%s|%s' % (val, val2)

    def bcancel_pr(self):
        self.reject()

    def bsave_pr(self):
        val = '%s-%s' % (self.apo.text(), self.eos.text())
        if val == "00:00-00:00":
            val = ""
        self.accept()


class TWeekdays(Qw.QWidget):
    '''Weekdays selection ([1,1,1,1,1,0,0] 7 values 0 or 1, one per weekday)'''
    def __init__(self, val=["", "", "", "", "", "", ""], parent=None):
        '''pin: {'name': xx, 'vals': [1,1,1,1,1,1,1], 'dayNames': []}'''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.parent = parent
        self.setSizePolicy(
            Qw.QSizePolicy(
                Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Expanding))
        self.set(val)
        self.dayNames = WEEKDAYS
        self.setMinimumSize(Qc.QSize(WIDTH, HEIGH))
        self.setMaximumSize(Qc.QSize(WIDTH, HEIGH))
        self.setMinimumHeight(HEIGH)
        # MENU
        self.setContextMenuPolicy(Qc.Qt.ActionsContextMenu)
        editAction = Qw.QAction("5days 08:00-16:00", self)
        editAction.triggered.connect(self.set5days)
        self.addAction(editAction)
        deleteAction = Qw.QAction("Reset", self)
        deleteAction.triggered.connect(self.reset)
        self.addAction(deleteAction)

    def sizeHint(self):
        return Qc.QSize(WIDTH, HEIGH)

    def calc_total_week_hours(self):
        total_hours = 0
        for elm in self.grid:
            if elm != '':
                total_hours += calc_multiple_hours(elm)
        return total_hours

    def hint(self):
        # print(self.mapToGlobal(Qg.QCursor.pos()))
        return 'Total week hours %s' % self.calc_total_week_hours()

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
            frm = DayHours(self.dayNames[x], self.grid[x], self)
            if frm.exec_() == Qw.QDialog.Accepted:
                self.grid[x] = frm.get_vals()
                self.update()

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
            if cell != '':
                color = COLORON  # Qc.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qc.Qt.black)
                painter.setBrush(color)
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qc.Qt.black
                painter.restore()
            painter.setPen(Qc.Qt.black)
            painter.drawText(rect.adjusted(4, 3, -3, -3), self.dayNames[x])
            vals = cell.split('|')
            if len(vals) == 1:
                vals.append('')
            painter.drawText(rect.adjusted(4, 16, -3, -3), vals[0])
            painter.drawText(rect.adjusted(4, 29, -3, -3), vals[1])
            painter.drawRect(rect)
        self.setToolTip(self.hint())

    def get(self, strVal=True):
        if strVal:
            return str(self.grid).replace("'", '"').replace('"', '!')
        else:
            return self.grid

    def set(self, darray=None):
        # Set values to days vector. But first checks for
        # proper array length and type
        if darray is None or darray == '':
            darr = '["", "", "", "", "", "", ""]'
        else:
            darr = str(darray).replace('!', "'")
        tmparr = eval(darr)
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = ["", "", "", "", "", "", ""]
        self.update()

    def reset(self):
        'Set everything to Null'
        self.set(["", "", "", "", "", "", ""])

    def set5days(self):
        'Set Standard five days week'
        self.set(['08:00-16:00', '08:00-16:00', '08:00-16:00', '08:00-16:00',
                  '08:00-16:00', '', ''])
