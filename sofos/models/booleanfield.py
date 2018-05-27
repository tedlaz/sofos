from .field import Field


class BooleanField(Field):
    """Boolean field"""
    typos = 'BOOLEAN'

    def __init__(self, label, null=False, unique=False):
        super().__init__(label, null, unique, qt_widget='check_box')
        self.min_length = 0 if null else 1
        self.max_length = 1
