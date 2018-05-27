from .field import Field


class IntegerField(Field):
    """Integer fields"""
    typos = 'INTEGER'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='int')
        self.add_validator(self.validator_int)

    def validator_int(self, value):
        try:
            int(value)
            return True, 'Integer value'
        except Exception:
            return False, 'Not an integer value'
