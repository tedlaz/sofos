import PyQt5.QtCore as Qc

CONFIRMATIONS = False
GRLOCALE = Qc.QLocale(Qc.QLocale.Greek, Qc.QLocale.Greece)
MSG_RESET_DATE = u'Reset with right mouse click'
MIN_HEIGHT = 30
MAX_HEIGHT = 40
DATE_MAX_WIDTH = 120
SQLITE_DATE_FORMAT = 'yyyy-MM-dd'
GREEK_DATE_FORMAT = 'd/M/yyyy'
WEEKDAYS = ['Δε', 'Τρ', 'Τε', 'Πέ', 'Πα', 'Σά', 'Κυ']
WEEKDAYS_FULL = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη',
                 'Παρασκευή', 'Σάββατο', 'Κυριακή']
MSG_SELECT_DAYS = 'Select working days\nReset with right mouse click'
BLANK, GREEN = range(2)
