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

    def test_TDateEmpty_02(self):
        dempty = qt.TDateEmpty('2017-01-01')
        self.assertEqual(dempty.get(), '2017-01-01')
        QTest.mouseClick(dempty, Qc.Qt.RightButton)
        QTest.mouseClick(dempty, Qc.Qt.LeftButton)
        dempty.menu_calendar()

    def test_TIntegerSpin_01(self):
        isp = qt.TIntegerSpin()
        self.assertEqual(isp.get(), 0)
        isp.set(None)
        self.assertEqual(isp.get(), 0)

    def test_TNumeric_01(self):
        qnu = qt.TNumeric()
        self.assertEqual(str(qnu.get()), '0.00')

    def test_TNumeric_02(self):
        qnu = qt.TNumeric(12.34)
        self.assertEqual(str(qnu.get()), '12.34')

    def test_TNumeric_03(self):
        qnu = qt.TNumeric(None)
        self.assertEqual(str(qnu.get()), '0.00')

    def test_TNumericSpin_01(self):
        qns = qt.TNumericSpin(None)
        self.assertEqual(str(qns.get()), '0.00')

    def test_TText_01(self):
        ttx = qt.TText(None)
        self.assertEqual(ttx.get(), '')
        ttx.set('')
        self.assertEqual(ttx.get(), '')
        ttx.set(' test again  ')
        self.assertEqual(ttx.get(), 'test again')

    def test_TTextLine_01(self):
        ttl = qt.TTextLine(None)
        self.assertEqual(ttl.get(), '')
        ttl.set('')
        self.assertEqual(ttl.get(), '')
        ttl.set(' test ')
        self.assertEqual(ttl.get(), 'test')

    def test_TInteger_01(self):
        tin = qt.TInteger(None)
        self.assertEqual(tin.get(), '0')
        tin.set('')
        self.assertEqual(tin.get(), '0')
        tin.set(100)
        self.assertEqual(tin.get(), '100')

    def test_TIntegerKey_01(self):
        tink = qt.TIntegerKey(None)
        self.assertEqual(tink.get(), '')
        tink.set('')
        self.assertEqual(tink.get(), '')
        tink.set(100)
        self.assertEqual(tink.get(), '100')

    def test_TTextlineNum_01(self):
        ttln = qt.TTextlineNum()
        self.assertEqual(ttln.get(), '')
        ttln = qt.TTextlineNum(None)
        self.assertEqual(ttln.get(), '')
        ttln.set(' 1234 ')
        self.assertEqual(ttln.get(), '1234')

    def test_TYesNoCombo_01(self):
        ync = qt.TYesNoCombo(None)
        self.assertEqual(ync.get(), False)
        ync = qt.TYesNoCombo()
        self.assertEqual(ync.get(), False)
        ync.set(1)
        self.assertEqual(ync.get(), True)

    def test_TWeekdays_01(self):
        twd = qt.TWeekdays(None)
        self.assertEqual(twd.get(), '[!!, !!, !!, !!, !!, !!, !!]')
        # twd = qt.TWeekdays()
        # self.assertEqual(twd.get(), '[1, 1, 1, 1, 1, 0, 0]')
        # self.assertEqual(twd.get(False), [1, 1, 1, 1, 1, 0, 0])
        twd.set([1, 2])
        self.assertEqual(twd.get(), '[!!, !!, !!, !!, !!, !!, !!]')
        twd.set5days()
        self.assertEqual(twd.get(), '[!08:00-16:00!, !08:00-16:00!, !08:00-16:00!, !08:00-16:00!, !08:00-16:00!, !!, !!]')
        QTest.mouseClick(twd, Qc.Qt.RightButton)
        # QTest.mouseClick(twd, Qc.Qt.LeftButton)

    def test_TCombo_01(self):
        tcb = qt.TCombo(None, vlist=[(1, 'aa'), (2, 'bb')])
        self.assertEqual(tcb.get(), 1)
        tcb.set(1)
        self.assertEqual(tcb.get(), 1)
