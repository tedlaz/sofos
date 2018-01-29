"""
Main models library
"""
from . import gr
from . import database_functions as df
IGNORE = 'models'  # For final models file
QTW = ['int', 'text_button', 'combo', 'check_box', 'date', 'date_or_empty',
       'num', 'text_num', 'text', 'week_days', 'str']


class Field():
    typos = ''

    def __init__(self, label='', null=False, unique=False, default=None,
                 qt_widget='str'):
        self.label = label
        self.null = null
        self.unique = unique
        self.default = default
        self.qt_widget = qt_widget

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
        super().__init__(label, null, unique, qt_widget='str')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True


class CharNumField(Field):
    typos = 'TEXT'

    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text_num')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True

class DateField(Field):
    typos = 'DATE'

    def __init__(self, label, max_length=10, null=False, unique=False,
                 min_length=10):
        super().__init__(label, null, unique, qt_widget='date')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        if value[4] != '-':
            return False
        return True


class DateEmptyField(Field):
    typos = 'DATETIME'

    def __init__(self, label, max_length=10, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='date_or_empty')
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
        super().__init__(label, null, unique, default=default, qt_widget='int')

    def validate(self, value):
        return int(value)


class DecimalField(Field):
    typos = 'DECIMAL'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='num')

    def validate(self, value):
        return int(value)


class WeekdaysField(Field):
    typos = 'TEXT'

    def __init__(self, label, max_length=30, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='week_days')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True


class ForeignKey(Field):
    typos = 'INTEGER'

    def __init__(self, ftable, label, qt_widget='text_button',
                 null=False, unique=False):
        super().__init__(label, null, unique, qt_widget=qt_widget)
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
        self.id = ''

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

    def load(self, idv):
        sql = self.sql_select_by_id(idv)
        row_from_db = df.select_one(self.dbf, sql)
        if row_from_db:
            self.set_from_dict(row_from_db)

    def get_dict(self, with_id=False):
        if with_id:
            adic = {'id': self.id}
        else:
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

    def sql_save(self):
        validated, msg = self.validate()
        if not validated:
            return msg
        dvals = self.get_dict()
        if self.id is None or self.id == '':
            sqt = 'INSERT INTO %s(%s) VALUES(%s);'
            flds = ', '.join(list(dvals.keys()))
            vals = ', '.join(["'%s'" % i for i in list(dvals.values())])
            return sqt % (self.table_name(), flds, vals)
        else:
            sqt = "UPDATE %s SET %s WHERE id='%s';"
            sts = ', '.join(["%s='%s'" % (i, j) for i, j in dvals.items()])
            return sqt % (self.table_name(), sts, self.id)

    def save(self):
        sql = self.sql_save()
        saved, lastid = df.cud(self.dbf, sql)
        if saved:
            if lastid:
                self.id = lastid

    @classmethod
    def save_meta(cls, dbf, dvals):
        if dvals['id'] is None or dvals['id'] == '':
            sqt = 'INSERT INTO %s(%s) VALUES(%s);'
            flds = ', '.join([i for i in dvals.keys() if i != 'id'])
            vals = ', '.join(["'%s'" % dvals[i] for i in dvals.keys() if i != 'id'])
            sql = sqt % (cls.table_name(), flds, vals)
        else:
            sqt = "UPDATE %s SET %s WHERE id='%s';"
            sts = ', '.join(["%s='%s'" % (i, j) for i, j in dvals.items()])
            sql = sqt % (cls.table_name(), sts, dvals['id'])
        return df.cud(dbf, sql)

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
        return 'SELECT * FROM %s' % cls.__name__.lower()

    @classmethod
    def search_by_id(cls, dbf, idv):
        sql = "SELECT * FROM %s WHERE id='%s'" % (cls.__name__, idv)
        return df.select_one(dbf, sql)

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

    @classmethod
    def select_all(cls, dbf):
        sql = 'SELECT * FROM %s' % cls.__name__.lower()
        return df.select_cols_rows(dbf, sql)

    @classmethod
    def search(cls, dbf, search_string):
        """Find records with many key words in search_string"""
        search_list = search_string.split()
        search_sql = []
        search_field = " || ' ' || ".join(cls.fields())
        sql1 = "SELECT * FROM %s \n" % cls.__name__.lower()
        where = ''
        for search_str in search_list:
            grup_str = gr.grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = 'WHERE'
        # if not search_string sql is simple select
        sql = sql1 + where + ' AND '.join(search_sql)
        adic = df.select_cols_rows(dbf, sql)
        return adic


def model_tables(models):
    """models: models.py from our project folder """
    tables = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    table_dict = {}
    for cls in tables:
        aaa = getattr(models, cls)
        table_dict[aaa.table_name()] = aaa
    return table_dict
