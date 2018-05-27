import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .. import gr
from .settings import MSG_RESET_DATE
from .settings import MIN_HEIGHT
from .settings import GREEK_DATE_FORMAT
from .settings import SQLITE_DATE_FORMAT


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
        self.setText('')
        if not gr.is_iso_date(iso_date) or len(iso_date) == 0:
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
