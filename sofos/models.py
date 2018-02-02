"""
Main models library
"""
from . import gr
from . import dbf as df
IGNORE = 'models'  # For final models file
QTW = ['int', 'text_button', 'combo', 'check_box', 'date', 'date_or_empty',
       'num', 'text_num', 'text', 'week_days', 'str']


class Field():
    """This is the base class of all field classes
    """
    typos = ''

    def __init__(self, label='', null=False, unique=False, default=None,
                 qt_widget='str'):
        self.label = label
        self.null = null
        self.unique = unique
        self.default = default
        self.qt_widget = qt_widget

    def sql(self, field):
        """sql create for field
        :param field: field name
        :return: sql
        """
        typ = self.typos
        null = '' if self.null else 'NOT NULL'
        unique = 'UNIQUE' if self.unique else ''
        defau = 'DEFAULT %s' % self.default if self.default is not None else ''
        tsq = '%s %s' % (field, typ)
        tsq += ' %s' % null if null != '' else ''
        tsq += ' %s' % unique if unique != '' else ''
        tsq += ' %s' % defau if defau != '' else ''
        return tsq

    def validate(self, value):
        """To be implemented by every child class"""
        return False


class CharField(Field):
    """char field """
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
    """Strings that take numeric values only (tax numbers, phones , etc)"""
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


class TextField(Field):
    """Long text fields"""
    typos = 'TEXT'

    def __init__(self, label, max_length=256, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True


class DateField(Field):
    """Date fields"""
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
    """Date or empty fields"""
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
    """Integer fields"""
    typos = 'INTEGER'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='int')

    def validate(self, value):
        return int(value)


class DecimalField(Field):
    """Decimal fields"""
    typos = 'DECIMAL'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='num')

    def validate(self, value):
        return int(value)


class WeekdaysField(Field):
    """Weekdays special fields"""
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
    """Foreign key fields"""
    typos = 'INTEGER'

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


class Model():
    """This class represents table. Most of the time it is used as meta class
    """
    def __init__(self, dbf):
        self.dbf = dbf
        self.id = ''

    def set(self, **kwargs):
        """set"""
        self.set_from_dict(kwargs)

    def set_from_dict(self, adict):
        """set from dictionary"""
        fields = self.fields()
        for key, value in adict.items():
            if key in fields or key == 'id':
                setattr(self, key, value)
                # self.data[key] = value
            else:
                raise ValueError

    def load(self, idv):
        """fill model with data from database"""
        sql = self.sql_select_by_id(idv)
        row_from_db = df.select_one(self.dbf, sql)
        if row_from_db:
            self.set_from_dict(row_from_db)

    def get_dict(self, with_id=False):
        """Get data from model in dictionary format"""
        if with_id:
            adic = {'id': self.id}
        else:
            adic = {}
        for field in self.fields():
            adic[field] = getattr(self, field)
        return adic

    def validate(self):
        """Validate data"""
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
        """create sql to save data to database"""
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
        """Save data to database"""
        sql = self.sql_save()
        saved, lastid = df.cud(self.dbf, sql)
        if saved:
            if lastid:
                self.id = lastid

    @classmethod
    def save_meta(cls, dbf, dva):
        """
        :param dbf: Database file
        :param dva: dictionary of values"""
        if dva['id'] is None or dva['id'] == '':
            sqt = 'INSERT INTO %s(%s) VALUES(%s);'
            flds = ', '.join([i for i in dva.keys() if i != 'id'])
            vls = ', '.join(["'%s'" % dva[i] for i in dva.keys() if i != 'id'])
            sql = sqt % (cls.table_name(), flds, vls)
        else:
            sqt = "UPDATE %s SET %s WHERE id='%s';"
            sts = ', '.join(["%s='%s'" % (i, j) for i, j in dva.items()])
            sql = sqt % (cls.table_name(), sts, dva['id'])
        return df.cud(dbf, sql)

    @classmethod
    def field(cls, field_name):
        """Get field object from field_name
        :param field_name: Field name
        """
        return getattr(cls, field_name)

    @classmethod
    def field_labels(cls):
        """Get a dictionary of field labels
        :return: dictionary of the form: {'fld_name': fld_label, ...}
        """
        fields = cls.fields()
        field_labels_dic = {'id': 'Νο'}
        for field in fields:
            cfield = getattr(cls, field)
            field_labels_dic[field] = cfield.label
        return field_labels_dic

    @classmethod
    def fields(cls):
        """Get a list of field names"""
        return [i for i in cls.__dict__.keys() if i[:1] != '_' and i != 'Meta']

    @classmethod
    def sql_create(cls):
        """get sql for Table creation"""
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
        """Select sql
        :return: sql for simple table selection
        """
        return 'SELECT * FROM %s' % cls.__name__.lower()

    @classmethod
    def search_by_id(cls, dbf, idv):
        """Search for a specific record by id

        :param dbf: Database file
        :param idv: the id to find
        :return: a dictionary with data or None (if not found)
        """
        sql = "SELECT * FROM %s WHERE id='%s'" % (cls.__name__, idv)
        return df.select_one(dbf, sql)

    @classmethod
    def search_by_id_deep(cls, dbf, idv):
        """Search for a specific record by id deep. Deep means that it returns
           every data from every parent table it finds.

        :param dbf: Database file
        :param idv: the id to find
        :return: a dictionary with data or None (if not found)
        """
        data = cls.sql_select_all_deep(dbf)
        sql = "%s WHERE %s.id='%s'" % (data['sql'], cls.__name__, idv)
        return df.select_one(dbf, sql)

    @classmethod
    def table_label(cls):
        """Get table label"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'table_label'):
                return cls.Meta.table_label
        return cls.__name__

    @classmethod
    def unique_together(cls):
        """unique_together is a Meta attribute to create sql unique values"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'unique_together'):
                return cls.Meta.unique_together
        return ''

    @classmethod
    def table_name(cls):
        """Get table name"""
        return cls.__name__.lower()

    @classmethod
    def select_all(cls, dbf):
        """Select all(To be corrected)"""
        sql = 'SELECT * FROM %s' % cls.__name__.lower()
        return df.select_cols_rows(dbf, sql)

    @classmethod
    def sql_select_all_deep(cls, dbf, field_list=None, label_list=None,
                            qt_widget_list=None, joins=None):
        """Returns sql with all relations of table

        :param dbf: Database file
        :param field_list: A list of fields (for recursion)
        :param label_list: A list of labels (for recursion)
        :param qt_widget_list: A list of qt_widgets (for recursion)
        :param joins: A list of joins (for recursion)
        """
        table_name = cls.__name__.lower()
        sqt = "SELECT %s\nFROM %s\n%s"
        flds = cls.fields()
        fld_dic = {table_name: []}
        field_list = field_list or ['%s.id' % table_name]
        label_list = label_list or ['ΑΑ']
        qt_widget_list = qt_widget_list or ['int']
        joins = joins or []
        for fld in flds:
            object_fld = getattr(cls, fld)
            if object_fld.__class__.__name__ == 'ForeignKey':
                ftbl = object_fld.ftable.table_name()
                if object_fld.null:
                    intl = 'LEFT JOIN %s ON %s.id=%s.%s'
                else:
                    intl = 'INNER JOIN %s ON %s.id=%s.%s'
                joins.append(intl % (ftbl, ftbl, table_name, fld))
                fld_dic[table_name].append(
                    object_fld.ftable.sql_select_all_deep(
                        dbf, field_list, label_list, qt_widget_list, joins))
            else:
                fld_dic[table_name].append('%s.%s' % (table_name, fld))
                field_list.append('%s.%s' % (table_name, fld))
                label_list.append(object_fld.label)
                qt_widget_list.append(object_fld.qt_widget)
        sql = sqt % (', '.join(field_list), table_name, '\n'.join(joins))
        return {'sql': sql, 'labels': label_list, 'cols': field_list,
                'qt_widgets_types': qt_widget_list, 'colnum': len(field_list)}

    @classmethod
    def deep_fields(cls, lfields=None, llabels=None, lqtwids=None):
        """Not finished yet"""
        table_name = cls.__name__.lower()
        table_flds = cls.fields()
        lfields = lfields or ['%s.id' % table_name]
        llabels = llabels or ['Νο']
        lqtwids = lqtwids or ['int']
        ljoins = []
        for field in table_flds:
            obj_field = getattr(cls, field)
            if obj_field.__class__.__name__ == 'ForeignKey':
                fk_table = obj_field.ftable.table_name()
                if obj_field.null:
                    pass

    @classmethod
    def select_all_deep(cls, dbf):
        """Deep select all"""
        data = cls.sql_select_all_deep(dbf)
        rows = df.select_rows(dbf, data['sql'])
        data['rows'] = rows
        data['rownum'] = len(rows)
        return data

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

    @classmethod
    def search_deep(cls, dbf, search_string):
        """Deep search

        :param dbf: Database file
        :param search_string: search string
        """
        search_list = search_string.split()
        meta = cls.sql_select_all_deep(dbf)
        search_field = " || ' ' || ".join(meta['cols'])
        where = ''
        search_sql = []
        for search_str in search_list:
            grup_str = gr.grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = ' WHERE '
        sql = meta['sql'] + where + ' AND '.join(search_sql)
        rows = df.select_rows(dbf, sql)
        meta['rows'] = rows
        meta['rownum'] = len(rows)
        return meta


def model_tables(models):
    """models: models.py from our project folder

    :return: Dictionary

    return dictionary format::

        {table_name1: table_object1, ...}
    """
    tables = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    table_dict = {}
    for cls in tables:
        aaa = getattr(models, cls)
        table_dict[aaa.table_name()] = getattr(models, cls)
    return table_dict
