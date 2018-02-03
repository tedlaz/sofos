"""Module test_dategr"""
import unittest
from PyQt5.QtTest import QTest
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
from sofos import qt


class Tests(unittest.TestCase):

    def setUp(self):
        super(Tests, self).setUp()
        self.app = Qw.QApplication([])

    def tearDown(self):
        """Deletes the reference owned by self"""
        del self.app
        super(Tests, self).tearDown()

    def test_TCheckbox_01(self):
        chkbox = qt.TCheckbox()
        self.assertEqual(chkbox.get(), 0)

    def test_TCheckbox_02(self):
        chkbox = qt.TCheckbox()
        chkbox.set(1)
        self.assertEqual(chkbox.get(), 2)

    def test_TDate_01(self):
        date = qt.TDate()
        date.set('2017-01-13')
        self.assertEqual(date.get(), '2017-01-13')

    def test_TDateEmpty_01(self):
        dempty = qt.TDateEmpty()
        self.assertEqual(dempty.get(), '')

    def test_TNumeric_01(self):
        qnu = qt.TNumeric()
        self.assertEqual(str(qnu.get()), '0.00')

    def test_TNumeric_02(self):
        qnu = qt.TNumeric(12.34)
        self.assertEqual(str(qnu.get()), '12.34')

    def test_TNumeric_03(self):
        qnu = qt.TNumeric(None)
        self.assertEqual(str(qnu.get()), '0.00')