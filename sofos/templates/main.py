#!/usr/bin/env python
import sys
import os
import importlib
import pkgutil
from datetime import datetime
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import main_rc
from sofos import qt
from sofos import database
from settings import setup
import models as md
import zforms
# from forms import Form1
qt.CONFIRMATIONS = setup['confirmations']
BDIR = os.path.dirname(md.__file__)
INIT_DB = os.path.join(BDIR, 'init_db.sql')


def get_modules():
    form_path = os.path.dirname(zforms.__file__)
    form_names = [name for _, name, _ in pkgutil.iter_modules([form_path])]
    modules = {}
    for form in form_names:
        my_module = importlib.import_module('zforms.%s' % form)
        try:
            modules[my_module.NAME] = my_module
        except AttributeError as err:
            print(err)
    return modules


class MainWindow(Qw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(Qg.QIcon(':/images/app.png'))
        self.database = database.Database(md)
        self.settings = Qc.QSettings()
        self.mdiArea = Qw.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qc.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qc.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = Qc.QSignalMapper(self)
        self.windowMapper.mapped[Qw.QWidget].connect(self.setActiveSubWindow)
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def newFile(self):
        options = Qw.QFileDialog.Options()
        filtyp = "sql3 App Files (*.%s)" % setup['db_suffix']
        filename, _ = Qw.QFileDialog.getSaveFileName(
            self,
            "Create New Database",
            self.database.dbf,
            filtyp,
            options=options)
        if filename:
            if not filename.endswith('.%s' % setup['db_suffix']):
                filename = '%s.%s' % (filename, setup['db_suffix'])
            success, msg = self.database.create_database(filename, INIT_DB)
            if success:
                self.update_dbf(self.database.dbf)
                Qw.QMessageBox.information(
                    self,
                    setup['db_creation_title'],
                    msg)
            else:
                os.remove(filename)
                Qw.QMessageBox.critical(
                    self,
                    setup['db_creation_title'],
                    str(msg))

    def update_dbf(self, dbf):
        if not dbf:
            self.tablemenu.setEnabled(False)
            for menu in self.ufmenu.values():
                menu.setEnabled(False)
        elif not self.database.set_database(dbf):
            Qw.QMessageBox.critical(
                self,
                "Πρόβλημα",
                "Η βάση δεδομένων %s δεν είναι συμβατή" % dbf)
            self.tablemenu.setEnabled(False)
            for menu in self.ufmenu.values():
                menu.setEnabled(False)
        else:
            self.tablemenu.setEnabled(True)
            for menu in self.ufmenu.values():
                menu.setEnabled(True)
            self.setWindowTitle('%s %s' % (setup['application_title'], dbf))

    def open(self):
        filtyp = "sql3 App Files (*.%s)" % setup['db_suffix']
        filename, _ = Qw.QFileDialog.getOpenFileName(
            self,
            'Open database',
            self.database.dbf,
            filtyp)
        if filename:
            self.update_dbf(filename)

    def about(self):
        Qw.QMessageBox.about(
            self,
            setup['about_title'],
            setup['app_desc'])

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)
        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)
        for i, window in enumerate(windows):
            child = window.widget()
            text = "%d %s" % (i + 1, child.table_label())
            if i < 9:
                text = '&' + text
            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createAutoFormTbl(self, table):
        child = qt.AutoFormTable(self.database.table_object(table))
        # child = qt.AutoFormTableWidget(self.database.table_object(table))
        self.mdiArea.addSubWindow(child)
        child.show()

    def refresh_forms(self):
        for window in self.mdiArea.subWindowList():
            form = window.widget()
            if hasattr(form, '_populate'):
                form._populate()

    def backup(self):
        tim = datetime.now().isoformat()
        tsr = tim.replace('-', '').replace('T', '').replace(':', '')[:12]
        filename = '%s.%s.sql' % (self.database.dbf, tsr)
        success, msg = self.database.backup_database()
        if success:
            Qw.QMessageBox.information(self, 'Database Backup', msg)
        else:
            os.remove(filename)
            Qw.QMessageBox.critical(self, 'Database Backup Error', str(msg))

    def createActions(self):
        self.newAct = Qw.QAction(
            Qg.QIcon(':/images/new.png'),
            "&New",
            self,
            shortcut=Qg.QKeySequence.New,
            statusTip="Create a new database",
            triggered=self.newFile)

        self.openAct = Qw.QAction(
            Qg.QIcon(':/images/open.png'),
            "&Open...",
            self,
            shortcut=Qg.QKeySequence.Open,
            statusTip="Open an existing database",
            triggered=self.open)

        self.backupAct = Qw.QAction(
            "Backup Database",
            self,
            statusTip="Backup current database",
            triggered=self.backup)

        self.exitAct = Qw.QAction(
            "E&xit",
            self,
            shortcut=Qg.QKeySequence.Quit,
            statusTip="Exit the application",
            triggered=Qw.QApplication.instance().closeAllWindows)

        self.closeAct = Qw.QAction(
            "Cl&ose",
            self,
            statusTip="Close the active window",
            triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = Qw.QAction(
            "Close &All",
            self,
            statusTip="Close all the windows",
            triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = Qw.QAction(
            "&Tile",
            self,
            statusTip="Tile the windows",
            triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = Qw.QAction(
            "&Cascade",
            self,
            statusTip="Cascade the windows",
            triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = Qw.QAction(
            "Ne&xt",
            self,
            shortcut=Qg.QKeySequence.NextChild,
            statusTip="Move the focus to the next window",
            triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = Qw.QAction(
            "Pre&vious",
            self,
            shortcut=Qg.QKeySequence.PreviousChild,
            statusTip="Move the focus to the previous window",
            triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = Qw.QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = Qw.QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self.aboutQtAct = Qw.QAction(
            "About &Qt",
            self,
            statusTip="Show the Qt library's About box",
            triggered=Qw.QApplication.instance().aboutQt)
        # Autoform actions here
        self.tblact = {}
        self.mapper = {}
        for tbl, lbl in self.database.table_labels(True).items():
            self.mapper[tbl] = Qc.QSignalMapper(self)
            self.tblact[tbl] = Qw.QAction(lbl, self)
            self.tblact[tbl].setStatusTip('open %s' % lbl)
            self.mapper[tbl].setMapping(self.tblact[tbl], tbl)
            self.tblact[tbl].triggered.connect(self.mapper[tbl].map)
            self.mapper[tbl].mapped['QString'].connect(self.createAutoFormTbl)
        # uforms actions here
        self.ufactions = {}
        self.ufactionm = {}
        self.ufmodules = get_modules()
        for mnam, module in self.ufmodules.items():
            self.ufactionm[mnam] = Qc.QSignalMapper(self)
            self.ufactions[mnam] = Qw.QAction(module.TITLE, self)
            self.ufactions[mnam].setStatusTip('open %s' % module.TITLE)
            self.ufactionm[mnam].setMapping(self.ufactions[mnam], mnam)
            self.ufactions[mnam].triggered.connect(self.ufactionm[mnam].map)
            self.ufactionm[mnam].mapped['QString'].connect(self.create_uform)
            self.ufactions[mnam].menu = module.MENU

    def create_uform(self, mnam):
        uform = self.ufmodules[mnam].UForm(self.database)
        self.mdiArea.addSubWindow(uform)
        uform.show()

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        # action = self.fileMenu.addAction("Switch layout direction")
        # action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.backupAct)
        self.fileMenu.addAction(self.exitAct)
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.tablemenu = self.menuBar().addMenu("&Tables")
        for act in self.tblact:
            self.tablemenu.addAction(self.tblact[act])
        self.ufmenu = {}
        # self.menuBar().addMenu("&UFActions")
        for ufact in self.ufactions.values():
            if ufact.menu not in self.ufmenu:
                self.ufmenu[ufact.menu] = self.menuBar().addMenu(ufact.menu)
            self.ufmenu[ufact.menu].addAction(ufact)
        # self.custom_forms_menu = self.menuBar().addMenu("&Custom Forms")
        # self.custom_forms_menu.addAction(self.form1_action)
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        dbf = self.settings.value("dbf", defaultValue=None)
        self.update_dbf(dbf)
        pos = self.settings.value('pos', Qc.QPoint(200, 200))
        size = self.settings.value('size', Qc.QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        self.settings.setValue('dbf', self.database.dbf)
        self.settings.setValue('pos', self.pos())
        self.settings.setValue('size', self.size())
        # self.settings.setValue("editor/wrapMargin", 68)

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = Qc.QFileInfo(fileName).canonicalFilePath()
        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qc.Qt.LeftToRight:
            Qw.QApplication.setLayoutDirection(Qc.Qt.RightToLeft)
        else:
            Qw.QApplication.setLayoutDirection(Qc.Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)


def run():
    app = Qw.QApplication(sys.argv)
    app.setOrganizationName(setup["organization_name"])
    app.setOrganizationDomain(setup["organization_domain"])
    app.setApplicationName(setup["application_name"])
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
