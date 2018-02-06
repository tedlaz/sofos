"""Greek language functions"""
import decimal
import textwrap
import os
TGR = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩςάέήίϊΐόύϋΰώΆΈΉΊΪΌΎΫΏ"
TEN = "abgdezh8iklmn3oprstyfx4wABGDEZH8IKLMN3OPRSTYFX4WsaehiiioyyywAEHIIOYYW"


def isNum(val):  # is val number or not
    """Check if val is number or not

    :param val: value to check

    :return: True if val is number else False
    """
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)

    :param poso: the number to transofrm to decimal
    :param decimals: Number of decimals

    :return: A decimal number with specific number of decimal digits
    """
    poso = 0 if (poso is None) else poso
    tmp = decimal.Decimal(poso) if isNum(poso) else decimal.Decimal('0')
    tmp = decimal.Decimal(0) if decimal.Decimal(0) else tmp
    return tmp.quantize(decimal.Decimal(10) ** (-1 * decimals))


def triades(txt, separator='.'):
    """Help function to split digits to thousants (123456 becomes 123.456)

    :param txt: text to split
    :param separator: The separator to use

    :return: txt separated by separator in group of three

    Example::

        >>> import gr
        >>> gr.triades('abcdefg')
        'a.bcd.efg'
        >>> gr.triades('abcdefg', separator='|')
        'a|bcd|efg'
    """
    return separator.join(textwrap.wrap(txt[::-1], 3))[::-1]


def dec2gr(poso, decimals=2, zero_as_space=False):
    """Returns string formatted as Greek decimal (1234.56 becomes 1.234,56)

    :param poso: number to format
    :param decimals: Number of decimal digits
    :param zero_as_space: if True then zero values become one space

    :return: Greek formatted number

    Example::

        >>> import gr
        >>> gr.dec2gr('-2456')
        '2.456,00'
        >>> gr.dec2gr(0, zero_as_space=True)
        ' '
    """
    dposo = dec(poso, decimals)
    if dposo == dec(0):
        if zero_as_space:
            return ' '
        else:
            return '0'
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


def gr2dec(poso, decimals=2):
    """Returns decimal (12.345,67 becomes 12345.67)

    :param poso: text Greek formatted number
    :param decimals: decimal digits

    :return: Decimal number
    """
    st = poso.replace('.', '')
    ds = st.replace(',', '.')
    return dec(ds, decimals)


def is_integer(val):
    """True if integer False otherwise"""
    if not isNum(val):
        return False
    dval = dec(val, 5)
    if dval - int(dval) != 0:
        return False
    return True


def is_positive_integer(val):
    """True if positive integer False otherwise"""
    if not is_integer(val):
        return False
    if dec(val) <= 0:
        return False
    return True


def grup(txtval):
    """Trasforms a string to uppercase special for Greek comparison
    """
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
    adi = dict(zip(ar1, ar2))
    return ''.join([adi.get(letter, letter.upper()) for letter in txtval])


def cap_first_letter(txt):
    """Capitalize first letter.

    Example::

        >>> import gr
        >>> gr.cap_first_letter('abcd')
        'Abcd'
    """
    lejeis = txt.split()
    ftxt = []
    for leji in lejeis:
        ftxt.append(leji.title())
    return ' '.join(ftxt)


def gr2en(txt, space=' '):
    """Greek to Greeglish

    :param txt: Text to translate to Greeglish
    :param space: If space == '' then capitalize txt
    """
    gdic = dict(zip(TGR, TEN))
    gdic[' '] = space
    if space == '':
        tmp = cap_first_letter(txt)
    else:
        tmp = txt
    ftxt = ''
    for char in tmp:
        if char in gdic:
            ftxt += gdic.get(char, char)
        else:
            ftxt += char
    return ftxt


def rename_file(fname, no_space=True):
    """Rename a file

    :param fname: file to rename
    :param no_space: remove spaces from filename

    :return: A filename in greekglish
    """
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
    """Check if strdate is isodate (yyyy-mm-dd)

    :param strdate: normally an iso formatted (yyyy-mm-dd) string

    :return: True if iso_date False else
    """
    if strdate is None:
        return False
    ldate = len(strdate)
    if ldate != 10:
        return False
    if strdate[4] != '-':
        return False
    if strdate[7] != '-':
        return False
    year, month, day = strdate.split('-')
    if not is_positive_integer(year):
        return False
    if not is_positive_integer(month):
        return False
    if not is_positive_integer(day):
        return False
    if int(month) > 12:
        return False
    if int(day) > 31:
        return False
    return True


def date2gr(date, no_trailing_zeros=False):
    """Create Greek Date

    :param date: iso date 'yyyy-mm-dd'
    :param date: iso_date
    :param no_trailing_zeros: Month, Day without trailing zeros

    :return: 'dd/mm/yyyy'

    Example::

        >>> import dategr
        >>> dategr.date2gr('2017-01-05)
        '05/01/2017'
        >>> dategr.dat2gr('2017-01-15, no_trailing_zeros=True)
        '5/1/2017'
    """
    assert is_iso_date(date)

    def remove_zero(stra):
        """Remove trailing zeros"""
        return stra[1:] if int(stra) < 10 else stra
    year, month, day = date.split('-')
    if no_trailing_zeros:
        month, day = remove_zero(month), remove_zero(day)
    return '{day}/{month}/{year}'.format(year=year, month=month, day=day)


def is_weekdays(value):
    """Return True if value is weekdays False else"""
    strval = str(value)
    try:
        val1 = eval(strval)
    except Exception:
        return False
    try:
        lval = list(val1)
    except TypeError:
        return False
    if len(lval) != 7:
        return False
    # Need to check every single value in thelist
    for elm in lval:
        try:
            int(elm)
        except TypeError:
            return False
    return True
