import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
from .settings import WEEKDAYS
from .settings import MSG_SELECT_DAYS
from .settings import MIN_HEIGHT
from .settings import BLANK
from .settings import GREEN


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
            return str(self.grid)
        else:
            return self.grid

    def set(self, darray=None):
        # Set values to days vector. But first checks for
        # proper array length and type
        if darray is None or darray == '':
            darr = '[0, 0, 0, 0, 0, 0, 0]'
        else:
            darr = str(darray)
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
