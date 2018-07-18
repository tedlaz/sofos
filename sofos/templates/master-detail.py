import PyQt5.QtWidgets as Qw
from sofos import qt
from sofos import database
import models as md


if __name__ == '__main__':
    import sys
    dbf = '/home/ted/devtest/ted1/skat.sql3'
    app = Qw.QApplication(sys.argv)
    database = database.Database(md)
    database.set_database(dbf)
    master = database.table_object('trans')
    detail = database.table_object('transdetails')
    frm = qt.MasterDetail(master, detail, 'tran')
    frm.show()
    appex = app.exec_()
    sys.exit(appex)
