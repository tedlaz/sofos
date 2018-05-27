"""Module test_dategr"""
import unittest
from sofos import models as md


class Tests(unittest.TestCase):

    def test_CharField_01(self):
        acf = md.CharField('label1', 5)
        self.assertEqual(acf.typos, 'TEXT')
        self.assertEqual(acf.label, 'label1')
        self.assertEqual(acf.sql('tst'), 'tst TEXT NOT NULL')
        self.assertEqual(acf.validate('tedlz'), (True, []))
        self.assertEqual(acf.validate('tedlaz')[0], False)

    def test_CharNumField_01(self):
        acn = md.CharNumField('numfield1', 5)
        self.assertEqual(acn.typos, 'TEXT')
        self.assertEqual(acn.sql('tst'), 'tst TEXT NOT NULL')
        self.assertEqual(acn.validate('tedlz')[0], False)
        self.assertEqual(acn.validate('12345')[0], True)
        self.assertEqual(acn.validate('123456')[0], False)

    def test_TextField_01(self):
        act = md.TextField('txtfield1')
        self.assertEqual(act.typos, 'TEXT')
        self.assertEqual(act.sql('tst'), 'tst TEXT NOT NULL')
        self.assertEqual(act.validate('tedlz')[0], True)

    def test_DateField_01(self):
        adf = md.DateField('datefield')
        self.assertEqual(adf.typos, 'DATE')
        self.assertEqual(adf.sql('tst'), 'tst DATE NOT NULL')
        self.assertEqual(adf.validate('2017-01-01')[0], True)
        self.assertEqual(adf.validate('sdfsf')[0], False)

    def test_DateEmptyField_01(self):
        adef = md.DateEmptyField('dateEmptyfield')
        self.assertEqual(adef.typos, 'DATETIME')
        self.assertEqual(adef.sql('tst'), 'tst DATETIME')
        self.assertEqual(adef.validate('2017-01-01')[0], True)
        self.assertEqual(adef.validate('sdf')[0], False)
        self.assertEqual(adef.validate('')[0], True)
        self.assertEqual(adef.validate(None)[0], True)

    def test_IntegerField_01(self):
        aif = md.IntegerField('Integer field')
        self.assertEqual(aif.typos, 'INTEGER')
        self.assertEqual(aif.sql('tst'), 'tst INTEGER NOT NULL DEFAULT 0')
        self.assertEqual(aif.validate(123)[0], True)

    def test_DecimalField_01(self):
        dfld = md.DecimalField('decfield')
        self.assertEqual(dfld.typos, 'DECIMAL')
        self.assertEqual(dfld.sql('tst'), 'tst DECIMAL NOT NULL DEFAULT 0')
        self.assertEqual(dfld.validate(123)[0], True)
        self.assertEqual(dfld.validate('123')[0], True)
        self.assertEqual(dfld.validate(123.23)[0], True)
        self.assertEqual(dfld.validate('123.45')[0], True)
        self.assertEqual(dfld.validate('12f')[0], False)
        self.assertEqual(dfld.validate('')[0], False)

    def test_WeekdaysField_01(self):
        wdf = md.WeekdaysField('weekdays field')
        self.assertEqual(wdf.typos, 'TEXT')
        self.assertEqual(wdf.sql('tst'), 'tst TEXT NOT NULL')
        self.assertTrue(wdf.validate('[1, 0, 0, 1, 1, 1, 0]')[0])
        self.assertFalse(wdf.validate('[1, 0, 0]')[0])

    def test_ForeignKey_01(self):
        class Ftable(md.Model):
            aa = md.CharField('tst', 10)
        fkv = md.ForeignKey(Ftable, 'test')
        self.assertEqual(fkv.typos, 'INTEGER')
        tsql = 'tst INTEGER NOT NULL REFERENCES ftable(id)'
        self.assertEqual(fkv.sql('tst'), tsql)
        self.assertTrue(fkv.validate(12)[0])
        self.assertTrue(fkv.validate('12')[0])
        self.assertFalse(fkv.validate('1221h')[0])
