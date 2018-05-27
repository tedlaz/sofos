from .. import gr
from .field import Field


class DateField(Field):
    """Date fields"""
    typos = 'DATE'

    def __init__(self, label, null=False, unique=False):
        super().__init__(label, null, unique, qt_widget='date')
        self.add_validator(self.validator_date)

    def validator_date(self, value):
        if gr.is_iso_date(value):
            return True, 'Date value ok'
        return False, 'Not date value'
