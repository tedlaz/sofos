"""
Main models library
"""
from . import gr
IGNORE = 'models'  # For final models file


class Field():
    typos = ''
    def __init__(self, label='', null=False, unique=False, default=None):
        self.label = label
        self.null = null
        self.unique = unique
        self.default = default

    def sql(self, field):
        typ = self.typos
        null = '' if self.null else 'NOT NULL'
        unique = 'UNIQUE' if self.unique else ''
        default = 'DEFAULT %s' % self.default if self.default is not None else ''
        tsq = '%s %s' % (field, typ)
        tsq += ' %s' % null if null != '' else ''
        tsq += ' %s' % unique if unique != '' else ''
        tsq += ' %s' % default if default != '' else ''
        return tsq

    def validate(self, value):
        return False


class CharField(Field):
    typos = 'TEXT'
    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique)
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True

class IntegerField(Field):
    typos = 'INTEGER'
    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default)

    def validate(self, value):
        return int(value)


class DecimalField(Field):
    typos = 'DECIMAL'
    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default)

    def validate(self, value):
        return int(value)


class ForeignKey(Field):
    typos = 'INTEGER'
    def __init__(self, ftable, label, null=False, unique=False):
        super().__init__(label, null, unique)
        # if not isinstance(ftable, Field):
            # raise ValueError
        self.ftable = ftable

    def sql(self, field):
        null = '' if self.null else 'NOT NULL'
        unique = 'UNIQUE' if self.unique else ''
        tsq = '%s INTEGER' % field
        tsq += ' %s' % null if null != '' else ''
        tsq += ' %s' % unique if unique != '' else ''
        tsq += ' REFERENCES %s(id)' % self.ftable.__name__.lower()
        return tsq


class Model():
    def __init__(self, dbf):
        self.dbf = dbf
        self.id = None
        # self.data = {'id': None}

    def set(self, **kwargs):
        self.set_from_dict(kwargs)

    def set_from_dict(self, adict):
        fields = self.fields()
        for key, value in adict.items():
            if key in fields or key == 'id':
                setattr(self, key, value)
                # self.data[key] = value
            else:
                raise ValueError

    def get_dict(self):
        adic = {}
        for field in self.fields():
            adic[field] = getattr(self, field)
        return adic

    def validate(self):
        errs = []
        ers = 'elm length is %s out of(%s, %s)'
        for elm in self.fields():
            if elm == 'id':
                continue
            else:
                elmlen = len(getattr(self, elm))
                mfd = self.field(elm)  # Meta field
                validated = mfd.min_length <= elmlen <= mfd.max_length
                if not validated:
                    errs.append(ers % (elmlen, mfd.min_length, mfd.max_length))
        if not errs:
            return True, 'Every field validated'
        else:
            return False, errs

    def prn(self):
        txtv = ''
        labels = self.field_labels()
        for key in self.data:
            if key == 'id':
                txtv += '%s: %s\n' % ('Νο', self.data[key] if self.data[key] is not None else '')
            else:
                txtv += '%s: %s\n' % (labels[key], self.data[key])
        return txtv

    @classmethod
    def field(cls, field_name):
        return getattr(cls, field_name)

    @classmethod
    def field_labels(cls):
        fields = cls.fields()
        field_labels_dic = {'id': 'Νο'}
        for field in fields:
            cfield = getattr(cls, field)
            field_labels_dic[field] = cfield.label
        return field_labels_dic

    @classmethod
    def fields(cls):
        return [i for i in cls.__dict__.keys() if i[:1] != '_' and i != 'Meta']

    @classmethod
    def sql_create(cls):
        _sq = "CREATE TABLE IF NOT EXISTS %s(\n" % cls.table_name()
        _sq += "id INTEGER PRIMARY KEY,\n"
        sq_ = "\n);\n\n"
        sqf = []
        u_fields = cls.unique_together()
        uniq = ',\nUNIQUE (%s)' % ','.join(u_fields) if u_fields else ''
        for field in cls.fields():
            cfield = getattr(cls, field)
            sqf.append(cfield.sql(field))
        return _sq + ',\n'.join(sqf) + uniq + sq_

    @classmethod
    def sql_select(cls):
        return 'SELECT * FROM %s' % cls.__name__

    @classmethod
    def sql_select_by_id(cls, idv):
        return "SELECT * FROM %s WHERE id='%s'" % (cls.__name__, idv)

    @classmethod
    def table_label(cls):
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'table_label'):
                return cls.Meta.table_label
        return cls.__name__

    @classmethod
    def unique_together(cls):
        '''unique_together is a Meta attribute to create sql unique values'''
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'unique_together'):
                return cls.Meta.unique_together
        return ''

    @classmethod
    def table_name(cls):
        return cls.__name__.lower()


def model_tables(models):
    """models: models.py from our project folder """
    tables = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    table_dict = {}
    for cls in tables:
        aaa = getattr(models, cls)
        table_dict[aaa.table_name()] = aaa
    return table_dict
