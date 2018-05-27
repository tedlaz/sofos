from .field import Field


class TextField(Field):
    """Long text fields"""
    typos = 'TEXT'

    def __init__(self, label, max_length=256, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text')
        self.min_length = min_length
        self.max_length = max_length
        self.add_validator(self.validator_txtsize)
