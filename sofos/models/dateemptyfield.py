from .. import gr
from .field import Field


class DateEmptyField(Field):
    """Date or empty fields"""
    typos = 'DATETIME'

    def __init__(self, label, null=True, unique=False):
        super().__init__(label, null, unique, qt_widget='date_or_empty')
        self.add_validator(self.validator_date_empty)

    def validator_date_empty(self, value):
        if value is None:
            return True, 'Ok empty value'
        if len(str(value)) == 0:
            if self.null:
                return True, 'Ok empty value'
            else:
                return False, 'Not null value allowed'
        else:
            if gr.is_iso_date(value):
                return True, 'Date value ok'
        return False, 'Not date value'
