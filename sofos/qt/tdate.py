import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .. import gr
from .settings import GREEK_DATE_FORMAT
from .settings import DATE_MAX_WIDTH
from .settings import MAX_HEIGHT
from .settings import GRLOCALE
from .settings import SQLITE_DATE_FORMAT


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
        if gr.is_iso_date(iso_date):
            yyy, mmm, ddd = iso_date.split('-')
            qdate = Qc.QDate()
            qdate.setDate(int(yyy), int(mmm), int(ddd))
            self.setDate(qdate)
        else:
            self.setDate(Qc.QDate.currentDate())

    def get(self):
        return '%s' % self.date().toString(SQLITE_DATE_FORMAT)
