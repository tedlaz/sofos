from .. import gr
from .field import Field


class CharNumField(Field):
    """Strings that take numeric values only (tax numbers, phones , etc)"""
    typos = 'TEXT'

    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text_num')
        self.min_length = min_length
        self.max_length = max_length
        self.add_validator(self.validator_positive_integer)
        self.add_validator(self.validator_txtsize)

    def validator_positive_integer(self, value):
        if not gr.is_positive_integer(value):
            return False, 'Not a positive integer'
        return True, 'value is a positive integer'
