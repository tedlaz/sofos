import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw


class MdiChild(Qw.QTextEdit):
    sequenceNumber = 1

    def __init__(self):
        super(MdiChild, self).__init__()
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.isUntitled = True

    def newFile(self):
        self.isUntitled = True
        self.curFile = "document%d.txt" % MdiChild.sequenceNumber
        MdiChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = Qc.QFile(fileName)
        if not file.open(Qc.QFile.ReadOnly | Qc.QFile.Text):
            Qw.QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False

        instr = Qc.QTextStream(file)
        Qw.QApplication.setOverrideCursor(Qc.Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        Qw.Application.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.document().contentsChanged.connect(self.documentWasModified)

        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = Qw.QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False
        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = Qc.QFile(fileName)
        if not file.open(Qc.QFile.WriteOnly | Qc.QFile.Text):
            Qw.QMessageBox.warning(self, "MDI",
                "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False
        outstr = Qc.QTextStream(file)
        Qw.QApplication.setOverrideCursor(Qc.Qt.WaitCursor)
        outstr << self.toPlainText()
        Qw.QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.document().isModified():
            ret = Qw.QMessageBox.warning(self, "MDI",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    Qw.QMessageBox.Save | Qw.QMessageBox.Discard | Qw.QMessageBox.Cancel)

            if ret == Qw.QMessageBox.Save:
                return self.save()

            if ret == Qw.QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = Qc.QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return Qc.QFileInfo(fullFileName).fileName()
