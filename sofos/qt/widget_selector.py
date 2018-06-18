from .tcheckbox import TCheckbox
from .tdate import TDate
from .tdateempty import TDateEmpty
# from .tintegerspin import TIntegerSpin
from .tnumeric import TNumeric
# from .tnumericspin import TNumericSpin
from .ttext import TText
from .ttextline import TTextLine
from .ttextline import TInteger
# from .ttextline import TIntegerKey
from .ttextline import TTextlineNum
# from .tyesnocombo import TYesNoCombo
from .tweekdays import TWeekdays
# from .tcombo import TCombo
from .tcombodb import TComboDB
from .ttextbutton import TTextButton


def wselector(field, parent):
    """Factory to create widgets

    :param field: object field
    :param parent: parent object

    :return: A customized qt widget
    """
    if field.qt_widget == 'int':
        return TInteger(parent=parent)
    elif field.qt_widget == 'text_button':
        return TTextButton(None, field.ftable, parent)
    elif field.qt_widget == 'combo':
        return TComboDB(field.default, field.ftable, parent)
    elif field.qt_widget == 'check_box':
        return TCheckbox(parent=parent)
    elif field.qt_widget == 'date':
        return TDate(parent=parent)
    elif field.qt_widget == 'date_or_empty':
        return TDateEmpty(parent=parent)
    elif field.qt_widget == 'num':
        return TNumeric(parent=parent)
    elif field.qt_widget == 'text_num':
        return TTextlineNum(parent=parent)
    elif field.qt_widget == 'text':
        return TText(parent=parent)
    elif field.qt_widget == 'week_days':
        return TWeekdays(parent=parent)
    elif field.qt_widget == 'str':
        return TTextLine(parent=parent)
    else:
        return TTextLine(parent=parent)


def widget_by_name(fld_name, parent, ftable=None):
    """Factory to create widgets

    :param field: object field
    :param parent: parent object

    :return: A customized qt widget
    """
    if fld_name == 'int':
        return TInteger(parent=parent)
    elif fld_name == 'text_button':
        return TTextButton(None, ftable, parent)
    elif fld_name == 'combo':
        return TComboDB(None, ftable, parent)
    elif fld_name == 'check_box':
        return TCheckbox(parent=parent)
    elif fld_name == 'date':
        return TDate(parent=parent)
    elif fld_name == 'date_or_empty':
        return TDateEmpty(parent=parent)
    elif fld_name == 'num':
        return TNumeric(parent=parent)
    elif fld_name == 'text_num':
        return TTextlineNum(parent=parent)
    elif fld_name == 'text':
        return TText(parent=parent)
    elif fld_name == 'week_days':
        return TWeekdays(parent=parent)
    elif fld_name == 'str':
        return TTextLine(parent=parent)
    else:
        return TTextLine(parent=parent)
