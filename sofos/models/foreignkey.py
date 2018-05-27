from .field import Field


class ForeignKey(Field):
    """Foreign key fields"""
    typos = 'INTEGER'
    fkey = True

    def __init__(self, ftable, label, qt_widget='text_button',
                 null=False, unique=False, default=None):
        super().__init__(label, null, unique, qt_widget=qt_widget,
                         default=default)
        self.ftable = ftable

    def sql(self, field):
        null = '' if self.null else 'NOT NULL'
        unique = 'UNIQUE' if self.unique else ''
        tsq = '%s INTEGER' % field
        tsq += ' %s' % null if null != '' else ''
        tsq += ' %s' % unique if unique != '' else ''
        tsq += ' REFERENCES %s(id)' % self.ftable.__name__.lower()
        return tsq

    def validate(self, value):
        if self.null:
            return (True, 'ok')
        try:
            int(value)
            result = (True, 'ok foreignkey is integer')
        except Exception:
            result = (False, 'Error foreignkey %s is not an integer' % value)
        return result
