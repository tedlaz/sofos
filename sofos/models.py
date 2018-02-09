"""Module Models
"""
import hashlib
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
        self.min_length = 0
        self.max_length = 0

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
        lval = len(value)
        if lval < self.min_length or lval > self.max_length:
            return False
        return True


class CharField(Field):
    """char field """
    typos = 'TEXT'

    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='str')
        self.min_length = min_length
        self.max_length = max_length


class CharNumField(Field):
    """Strings that take numeric values only (tax numbers, phones , etc)"""
    typos = 'TEXT'

    def __init__(self, label, max_length, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text_num')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        if not gr.is_positive_integer(value):
            return False
        return super().validate(value)


class TextField(Field):
    """Long text fields"""
    typos = 'TEXT'

    def __init__(self, label, max_length=256, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='text')
        self.min_length = min_length
        self.max_length = max_length


class DateField(Field):
    """Date fields"""
    typos = 'DATE'

    def __init__(self, label, null=False, unique=False):
        super().__init__(label, null, unique, qt_widget='date')

    def validate(self, value):
        return gr.is_iso_date(value)


class DateEmptyField(Field):
    """Date or empty fields"""
    typos = 'DATETIME'

    def __init__(self, label, null=False, unique=False):
        super().__init__(label, null, unique, qt_widget='date_or_empty')

    def validate(self, value):
        if value is None or value == '':
            return True
        return gr.is_iso_date(value)


class IntegerField(Field):
    """Integer fields"""
    typos = 'INTEGER'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='int')

    def validate(self, value):
        return gr.is_integer(value)


class DecimalField(Field):
    """Decimal fields"""
    typos = 'DECIMAL'

    def __init__(self, label='', null=False, unique=False, default=0):
        super().__init__(label, null, unique, default=default, qt_widget='num')

    def validate(self, value):
        return gr.isNum(value)


class WeekdaysField(Field):
    """Weekdays special fields"""
    typos = 'TEXT'

    def __init__(self, label, max_length=30, null=False, unique=False,
                 min_length=0):
        super().__init__(label, null, unique, qt_widget='week_days')
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        return gr.is_weekdays(value)


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

    def validate(self, value):
        """Value must always be integer"""
        return gr.is_integer(value)


class Model():
    """This class represents table. Most of the time it is used as meta class
    """
    __dbf__ = 'jj'

    @classmethod
    def table_name(cls):
        """Get table name"""
        return cls.__name__.lower()

    @classmethod
    def table_label(cls):
        """Get table label"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'table_label'):
                return cls.Meta.table_label
        return cls.__name__

    @classmethod
    def field_object(cls, field_name):
        """Get field object from field_name

        :param field_name: Field name
        """
        return getattr(cls, field_name)

    @classmethod
    def field_labels(cls):
        """Get a dictionary of field labels
        :return: dictionary of the form: {'fld_name': fld_label, ...}
        """
        field_labels_dic = {'id': 'Νο'}
        for field in cls.field_names():
            cfield = getattr(cls, field)
            field_labels_dic[field] = cfield.label
        return field_labels_dic

    @classmethod
    def field_names(cls):
        """Get a list of field names"""
        return [i for i in cls.__dict__.keys() if i[:1] != '_' and i != 'Meta']

    @classmethod
    def _unique_together(cls):
        """unique_together is a Meta attribute to create sql unique values"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'unique_together'):
                return cls.Meta.unique_together
        return ''

    @classmethod
    def repr_fields(cls):
        """Representation fields"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'repr_fields'):
                return cls.Meta.repr_fields
        return None

    @classmethod
    def sql_create(cls):
        """get sql for Table creation"""
        _sq = "CREATE TABLE IF NOT EXISTS %s(\n" % cls.table_name()
        _sq += "id INTEGER PRIMARY KEY,\n"
        sq_ = "\n);\n\n"
        sqf = []
        u_fields = cls._unique_together()
        uniq = ',\nUNIQUE (%s)' % ','.join(u_fields) if u_fields else ''
        for field in cls.field_names():
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
        flds = cls.repr_fields() or cls.field_names()
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

    # @classmethod
    # def deep_fields(cls, lfields=None, llabels=None, lqtwids=None):
    #     """Not finished yet"""
    #     table_name = cls.__name__.lower()
    #     table_flds = cls.fields()
    #     lfields = lfields or ['%s.id' % table_name]
    #     llabels = llabels or ['Νο']
    #     lqtwids = lqtwids or ['int']
    #     ljoins = []
    #     for field in table_flds:
    #         obj_field = getattr(cls, field)
    #         if obj_field.__class__.__name__ == 'ForeignKey':
    #             fk_table = obj_field.ftable.table_name()
    #             if obj_field.null:
    #                 pass

    @classmethod
    def save(cls, dbf, dva):
        """Save Data dictionary dva to database

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
        return df.save(dbf, sql)

    @classmethod
    def select_all(cls, dbf):
        """Select all(To be corrected)"""
        sql = 'SELECT * FROM %s' % cls.__name__.lower()
        return df.read(dbf, sql, 'cols_rows')

    @classmethod
    def select_all_deep(cls, dbf):
        """Deep select all"""
        metadata = cls.sql_select_all_deep(dbf)
        _, rows = df.read(dbf, metadata['sql'], 'rows')
        metadata['rows'] = rows
        metadata['rownum'] = len(rows)
        return metadata

    @classmethod
    def search(cls, dbf, search_string):
        """Find records with many key words in search_string"""
        search_list = search_string.split()
        search_sql = []
        search_field = " || ' ' || ".join(cls.field_names())
        sql1 = "SELECT * FROM %s \n" % cls.__name__.lower()
        where = ''
        for search_str in search_list:
            grup_str = gr.grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = 'WHERE'
        # if not search_string sql is simple select
        sql = sql1 + where + ' AND '.join(search_sql)
        adic = df.read(dbf, sql, 'cols_rows')
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
        success, rows = df.read(dbf, sql, 'rows')
        meta['rows'] = rows
        meta['rownum'] = len(rows)
        return meta

    @classmethod
    def search_by_id(cls, dbf, idv):
        """Search for a specific record by id

        :param dbf: Database file
        :param idv: the id to find

        :return: a dictionary with data or None (if not found)
        """
        sql = "SELECT * FROM %s WHERE id='%s'" % (cls.__name__, idv)
        success, record = df.read(dbf, sql, 'one')
        return record

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
        success, record = df.read(dbf, sql, 'one')
        return record
