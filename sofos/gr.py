"""Greek language functions"""
import decimal
import textwrap
import os
TGR = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩςάέήίϊΐόύϋΰώΆΈΉΊΪΌΎΫΏ"
TEN = "abgdezh8iklmn3oprstyfx4wABGDEZH8IKLMN3OPRSTYFX4WsaeiiiioyyywAEHIIOYYW"


def isNum(val):  # is val number or not
    """Check if val is number or not"""
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)"""
    poso = 0 if (poso is None) else poso
    tmp = decimal.Decimal(poso) if isNum(poso) else decimal.Decimal('0')
    tmp = decimal.Decimal(0) if decimal.Decimal(0) else tmp
    return tmp.quantize(decimal.Decimal(10) ** (-1 * decimals))


def triades(txt, separator='.'):
    '''Help function to split digits to thousants (123456 becomes 123.456)'''
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def dec2gr(poso, decimals=2, zero_as_space=False):
    '''Returns string formatted as Greek decimal (1234,56 becomes 1.234,56)'''
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
    sdposo = str(dposo)
    meion = '-'
    decimal_ceparator = ','
    prosimo = ''
    if sdposo.startswith(meion):
        prosimo = meion
        sdposo = sdposo.replace(meion, '')
    if '.' in sdposo:
        sint, sdec = sdposo.split('.')
    else:
        sint = sdposo
        decimal_ceparator = ''
        sdec = ''
    return prosimo + triades(sint) + decimal_ceparator + sdec


def is_positive_integer(val):
    '''True if positive integer False otherwise'''
    intv = 0
    try:
        intv = int(val)
    except ValueError:
        return False
    if intv <= 0:
        return False
    return True


def grup(txtval):
    '''Trasforms a string to uppercase special for Greek comparison'''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
    adi = dict(zip(ar1, ar2))
    return ''.join([adi.get(letter, letter.upper()) for letter in txtval])


def cap_first_letter(txt):
    '''Capitalize first letter'''
    lejeis = txt.split()
    ftxt = []
    for leji in lejeis:
        ftxt.append(leji.title())
    return ' '.join(ftxt)


def gr2en(txt, space=' '):
    '''Greek to Greeglish'''
    gdic = dict(zip(TGR, TEN))
    gdic[' '] = space
    found = False
    if space == '':
        tmp = cap_first_letter(txt)
    else:
        tmp = txt
    ftxt = ''
    for char in tmp:
        if char in gdic:
            found = True
        ftxt += gdic.get(char, char)
    if found:
        return ftxt
    return None


def rename_file(fname, no_space=True):
    '''Rename a file'''
    if no_space:
        space = ''
    else:
        space = '_'
    fnam, ext = os.path.splitext(fname)
    enam = gr2en(fnam, space)
    if ext:
        if enam:
            return ''.join([enam, ext])
    else:
        if enam:
            return enam


def is_iso_date(strdate):
    """Check if strdate is isodate (yyyy-mm-dd)"""
    if strdate is None:
        return False
    ldate = len(strdate)
    if ldate != 10:
        return False
    if strdate[4] != '-':
        return False
    if strdate[7] != '-':
        return False
    for number in strdate.split('-'):
        if not is_positive_integer(number):
            return False
    return True


def date2gr(date, removezero=False):
    """If removezero = True returns d/m/yyyy else dd/mm/yyyy"""
    assert is_iso_date(date)

    def remove_zero(stra):
        """Remove trailing zeros"""
        return stra[1:] if int(stra) < 10 else stra
    year, month, day = date.split('-')
    if removezero:
        month, day = remove_zero(month), remove_zero(day)
    return '{day}/{month}/{year}'.format(year=year, month=month, day=day)


class NamesTuples():
    def __init__(self, names, rows):
        self.names = names
        self.rows = rows
        self.lines = len(self.rows)
        self.number_of_columns = len(names)
        if rows:
            assert len(names) == len(rows[0])
    def list_of_dic(self):
        tmpl = []
        for row in self.rows:
            dic = {}
            for i, name in enumerate(self.names):
                dic[name] = row[i]
            tmpl.append(dic)
        return tmpl

    def idv(self):
        return self.list_of_dic()[0].get('id', '') if self.lines > 0 else ''

    def list_of_labels(self):
        return [name for name in self.names]

    def lbl(self, name):
        return name

    def names_tuples(self):
        return self.names, self.rows

    def labels_tuples(self):
        return self.list_of_labels(), self.rows

    def one(self, with_names=True):
        if self.lines > 0:
            dic = {}
            for i, name in enumerate(self.names):
                dic[name] = self.rows[0][i]
            return (self.names, dic) if with_names else dic

        return (self.names, {}) if with_names else {}

    def value(self, line, field):
        if field not in self.names:
            return None
        if line < self.lines:
            return self.list_of_dic()[line-1][field]
        return None

    def values(self, *fields):
        # Experimental Function
        if sum([1  for fld in fields if fld not in self.names]):
            return None
        return 'ok'

    def __str__(self):
        return '%s\n%s\n%s' % (self.names, self.list_of_labels(), self.rows)


'''
counter = 0

import os
def process_dir(directory, no_space=False):
    """process all files in the folder"""
    global counter
    for fname in os.listdir(directory):
        file_or_dir = directory + os.sep + fname
        if os.path.isdir(file_or_dir):
            process_dir(file_or_dir, no_space)
        else:
            enam = rename_file(fname, no_space)
            if enam:
                oldf = directory + os.sep + fname
                newf = directory + os.sep + enam
                counter += 1
                # os.rename(oldf, newf)
                print('%5s:%s|%s' % (counter, oldf, newf))
'''

if __name__ == '__main__':
    print(triades('123123'))
