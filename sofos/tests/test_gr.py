"""Module test_dategr"""
import unittest
from sofos import gr


class Tests(unittest.TestCase):
    def test_isNum_01(self):
        self.assertEqual(gr.isNum('12.35'), True)

    def test_isNum_02(self):
        self.assertEqual(gr.isNum('12,35'), False)

    def test_isNum_03(self):
        self.assertEqual(gr.isNum('12.35a'), False)

    def test_isNum_04(self):
        self.assertEqual(gr.isNum('-0'), True)

    def test_isNum_05(self):
        aaa = ['1', '2', '3']
        self.assertEqual(gr.isNum(aaa), False)

    def test_dec_01(self):
        self.assertEqual(float(gr.dec('12.34')), 12.34)

    def test_dec_02(self):
        self.assertEqual(float(gr.dec(12.34)), 12.34)

    def test_dec_03(self):
        self.assertEqual(float(gr.dec('12df')), 0)

    def test_dec_04(self):
        self.assertEqual(float(gr.dec(None)), 0)

    def test_dec_05(self):
        self.assertEqual(float(gr.dec(15.236344)), 15.24)

    def test_dec_06(self):
        self.assertNotEqual(float(gr.dec('tedd')), 1)

    def test_dec_07(self):
        self.assertEqual(float(gr.dec('tedd')), 0)

    def test_dec_08(self):
        self.assertEqual(str(gr.dec(12.2, decimals=0)), '12')

    def test_triades_01(self):
        self.assertEqual(gr.triades('abcdef'), 'abc.def')

    def test_triades_02(self):
        self.assertEqual(gr.triades('abcdefg'), 'a.bcd.efg')

    def test_triades_03(self):
        self.assertEqual(gr.triades('abcdefg', '|'), 'a|bcd|efg')

    def test_triades_04(self):
        self.assertEqual(gr.triades('ab'), 'ab')

    def test_triades_05(self):
        self.assertEqual(gr.triades('abc'), 'abc')

    def test_triades_06(self):
        self.assertEqual(gr.triades(''), '')

    def test_dec2gr_01(self):
        self.assertEqual(gr.dec2gr('-2456', 1), '-2.456,0')

    def test_dec2gr_02(self):
        self.assertEqual(gr.dec2gr('-0', 0), '0')

    def test_dec2gr_03(self):
        self.assertEqual(gr.dec2gr('123123123.45'), '123.123.123,45')

    def test_dec2gr_04(self):
        self.assertEqual(gr.dec2gr(123123123.45), '123.123.123,45')

    def test_dec2gr_05(self):
        self.assertEqual(gr.dec2gr('-0', zero_as_space=True), ' ')

    def test_dec2gr_06(self):
        self.assertEqual(gr.dec2gr('123123', decimals=0), '123.123')

    def test_gr2dec_01(self):
        self.assertEqual(gr.gr2dec('123.123.123,45'), gr.dec('123123123.45'))

    def test_gr2dec_02(self):
        self.assertEqual(gr.gr2dec('123,452'), gr.dec('123.45'))

    def test_gr2dec_03(self):
        self.assertEqual(gr.gr2dec('-123,452'), gr.dec('-123.45'))

    def test_is_integer_01(self):
        self.assertEqual(gr.is_integer(12), True)
        self.assertEqual(gr.is_integer('12'), True)
        self.assertEqual(gr.is_integer('12a'), False)
        self.assertEqual(gr.is_integer('-12'), True)
        self.assertEqual(gr.is_integer(-12), True)
        self.assertEqual(gr.is_integer(12.01), False)
        self.assertEqual(gr.is_integer('12.01'), False)
        self.assertEqual(gr.is_integer('0'), True)
        self.assertEqual(gr.is_integer(0), True)
        self.assertEqual(gr.is_integer(''), False)

    def test_is_positive_integer_01(self):
        self.assertEqual(gr.is_positive_integer(12), True)

    def test_is_positive_integer_02(self):
        self.assertEqual(gr.is_positive_integer(-12), False)

    def test_is_positive_integer_03(self):
        self.assertEqual(gr.is_positive_integer(0), False)

    def test_is_positive_integer_04(self):
        self.assertEqual(gr.is_positive_integer('abd'), False)

    def test_is_positive_integer_05(self):
        self.assertEqual(gr.is_positive_integer('12.35'), False)

    def test_is_positive_integer_06(self):
        self.assertEqual(gr.is_positive_integer('12'), True)

    def test_is_positive_integer_07(self):
        self.assertEqual(gr.is_positive_integer('-12'), False)

    def test_grup_01(self):
        self.assertEqual(gr.grup('Δοκιμή'), 'ΔΟΚΙΜΗ')

    def test_grup_02(self):
        self.assertEqual(gr.grup('this02ένας'), 'THIS02ΕΝΑΣ')

    def test_cap_first_letter_01(self):
        self.assertEqual(gr.cap_first_letter('ted'), 'Ted')

    def test_cap_first_letter_02(self):
        self.assertEqual(gr.cap_first_letter('γεωργία'), 'Γεωργία')

    def test_gr2en_01(self):
        self.assertEqual(gr.gr2en('δοκιμή'), 'dokimh')

    def test_rename_file_01(self):
        self.assertEqual(gr.rename_file('δοκιμή'), 'Dokimh')

    def test_rename_file_02(self):
        self.assertEqual(gr.rename_file('δοκ.mia', False), 'dok.mia')

    def test_gr2en_03(self):
        self.assertEqual(gr.gr2en('δοκιμήd', space=''), 'Dokimhd')

    def test_gr2en_04(self):
        self.assertEqual(gr.gr2en('δοκιμήd', space=''), 'Dokimhd')

    def test_is_iso_date_01(self):
        self.assertEqual(gr.is_iso_date('2017-01-21'), True)

    def test_is_iso_date_02(self):
        self.assertEqual(gr.is_iso_date('2017-21-01'), False)

    def test_is_iso_date_03(self):
        self.assertEqual(gr.is_iso_date('2017-12-31'), True)

    def test_is_iso_date_04(self):
        self.assertEqual(gr.is_iso_date('2017-12-32'), False)

    def test_is_iso_date_05(self):
        self.assertEqual(gr.is_iso_date('δοκ.μια'), False)

    def test_is_iso_date_06(self):
        self.assertEqual(gr.is_iso_date(None), False)

    def test_is_iso_date_07(self):
        self.assertEqual(gr.is_iso_date('2017-0123-'), False)

    def test_is_iso_date_08(self):
        self.assertEqual(gr.is_iso_date('201730123-'), False)

    def test_is_iso_date_09(self):
        self.assertEqual(gr.is_iso_date('abcd-ef-gh'), False)

    def test_is_iso_date_10(self):
        self.assertEqual(gr.is_iso_date('2017-ef-gh'), False)

    def test_is_iso_date_11(self):
        self.assertEqual(gr.is_iso_date('2017-01-gh'), False)

    def test_date2gr_01(self):
        self.assertEqual(gr.date2gr('2017-12-31'), '31/12/2017')

    def test_date2gr_02(self):
        self.assertEqual(gr.date2gr('2017-02-01'), '01/02/2017')

    def test_date2gr_03(self):
        self.assertEqual(gr.date2gr('2017-02-01', no_trailing_zeros=True),
                         '1/2/2017')

    def test_is_weekdays_01(self):
        self.assertFalse(gr.is_weekdays(''))
        self.assertFalse(gr.is_weekdays('[1, 2]'))
        self.assertFalse(gr.is_weekdays([1, 1]))
        self.assertFalse(gr.is_weekdays([1, 1, 1, 1, 1, 1]))
        self.assertTrue(gr.is_weekdays('[1, 1, 1, 1, 1, 1, 1]'))
        self.assertTrue(gr.is_weekdays([1, 1, 1, 1, 1, 1, 1]))
