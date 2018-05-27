from .field import Field


class CharField(Field):
    """char field """
    typos = 'TEXT'

    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='str')
        self.min_length = min_length
        self.max_length = max_length
        self.add_validator(self.validator_txtsize)
