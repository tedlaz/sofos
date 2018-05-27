from .. import gr
from .field import Field


class DecimalField(Field):
    """Decimal fields"""
    typos = 'DECIMAL'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='num')
        self.add_validator(self.validator_d)

    def validator_d(self, value):
        result = gr.isNum(value)
        if result:
            return True, 'ok value is Number'
        else:
            return False, 'Error, value is not a Number'
