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
