from .field import Field


class WeekdaysField(Field):
    """Weekdays special fields"""
    typos = 'TEXT'

    def __init__(self, label, max_length=30, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='week_days')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, values):
        result = len(eval(values.replace('!', "'"))) == 7
        if result:
            return True, 'ok It is array'
        return False, 'Error, it is not an array'
