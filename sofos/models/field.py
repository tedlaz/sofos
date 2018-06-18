"""Abstract class Field"""
from .. import qt


class Field():
    """This is the base class of all field classes
    """
    typos = ''
    fkey = False

    def __init__(self, label='', null=False, unique=False, default=None,
                 qt_widget='str'):
        self.label = label
        self.null = null
        self.unique = unique
        self.default = default
        self.qt_widget = qt_widget
        self.min_length = 0
        self.max_length = 0
        self.validators = []

    def qwl(self, parent):
        return qt.widget_selector.wselector(self, parent)

    @property
    def is_foreign_key(self):
        return self.__class__.__name__ == 'ForeignKey'

    def sql(self, field):
        """sql create for field

        :param field: field name

        :return: sql
        """
        null = '' if self.null else 'NOT NULL'
        unique = 'UNIQUE' if self.unique else ''
        defau = 'DEFAULT %s' % self.default if self.default is not None else ''
        tsq = '%s %s' % (field, self.typos)
        tsq += ' %s' % null if null != '' else ''
        tsq += ' %s' % unique if unique != '' else ''
        tsq += ' %s' % defau if defau != '' else ''
        return tsq

    def add_validator(self, validation_function):
        self.validators.append(validation_function)

    def validate(self, value):
        if self.unique or not self.null:
            self.min_length = 1
        errors = []
        validated = True
        for validator in self.validators:
            passed, msg = validator(value)
            msg = '%s: %s' % (validator.__name__, msg)
            if not passed:
                errors.append(msg)
                validated = False
        return validated, errors

    def validator_txtsize(self, val):
        lval = len(str(val))
        if self.min_length <= lval <= self.max_length:
            return True, 'Size is Ok'
        else:
            return False, 'Size is out of allowed margins'
