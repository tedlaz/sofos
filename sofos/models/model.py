"""Module Models
"""
from .. import gr
from .. import dbf as df
IGNORE = 'models'  # For final models file
QTW = ['int', 'text_button', 'combo', 'check_box', 'date', 'date_or_empty',
       'num', 'text_num', 'text', 'week_days', 'str']


class Model():
    """This class represents table. Mostly it is used as a meta class
    """
    __dbf__ = None

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
    def table_child_name(cls):
        """If table has child table return child table name"""
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'table_child_name'):
                return cls.Meta.table_child_name.lower()
        return ''

    @classmethod
    def field_object(cls, field_name):
        """Get field object from field_name

        :param field_name: Field name
        """
        if hasattr(cls, field_name):
            return getattr(cls, field_name)
        return None

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
    def labels(cls):
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
    def field_objects(cls):
        dicf = {}
        for fname in cls.field_names():
            dicf[fname] = cls.field_object(fname)
        return dicf

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
        """Representation fields
        """
        if 'Meta' in cls.__dict__.keys():
            meta = getattr(cls, 'Meta')
            if hasattr(meta, 'repr_fields'):
                return cls.Meta.repr_fields
        return cls.field_names()

    @classmethod
    def sql_create(cls):
        """get sql for Table creation"""
        _sq = "CREATE TABLE IF NOT EXISTS %s(\n" % cls.table_name()
        _sq += "id INTEGER PRIMARY KEY,\n"
        sq_ = "\n);\n\n"
        sql_fields = []
        u_fields = cls._unique_together()
        uniq = ',\nUNIQUE (%s)' % ','.join(u_fields) if u_fields else ''
        for field in cls.field_names():
            cfield = getattr(cls, field)
            sql_fields.append(cfield.sql(field))
        return _sq + ',\n'.join(sql_fields) + uniq + sq_

    @classmethod
    def sql_select(cls):
        """Select sql
        :return: sql for simple table selection
        """
        return 'SELECT * FROM %s' % cls.__name__.lower()

    @classmethod
    def deep_labels(cls, alias=None):
        # tbl = cls.__name__.lower()
        lbl = []
        for field_name in cls.field_names():
            fld = cls.field_object(field_name)
            if fld.is_foreign_key:
                lbl += fld.ftable.deep_labels()
            else:
                lbl.append(fld.label)
        return lbl

    @classmethod
    def deep_labels2(cls):
        lbl = {}
        for field_name in cls.field_names():
            fld = cls.field_object(field_name)
            if fld.is_foreign_key:
                lbl = {**lbl, **fld.ftable.deep_labels2()}
            else:
                lbl['%s.%s' % (cls.table_name(), field_name)] = fld.label
        return lbl

    @classmethod
    def deep_widgets(cls, alias=None):
        lbl = []
        for field_name in cls.field_names():
            fld = cls.field_object(field_name)
            if fld.is_foreign_key:
                lbl += fld.ftable.deep_widgets(field_name)
            else:
                lbl.append(fld.qt_widget)
        return lbl

    @classmethod
    def deep_fields(cls, alias=None):
        tbl = cls.__name__.lower()
        tvl = []
        for field_name in cls.field_names():
            fld = cls.field_object(field_name)
            if fld.is_foreign_key:
                tvl += fld.ftable.deep_fields(field_name)
            else:
                tvl.append('%s.%s' % (alias or tbl, field_name))
        return tvl

    @classmethod
    def deep_joins(cls, alias=None):
        tbl = cls.__name__.lower()
        atbl = alias or tbl
        joins = []
        for fname in cls.field_names():
            fld = cls.field_object(fname)
            if fld.is_foreign_key:
                ftable = fld.ftable.table_name()
                if fld.null:
                    intl = 'LEFT JOIN %s AS %s ON %s.id=%s.%s'
                else:
                    intl = 'INNER JOIN %s AS %s ON %s.id=%s.%s'
                joins.append(intl % (ftable, fname, fname, atbl, fname))
                joins += fld.ftable.deep_joins(fname)
        return joins

    @classmethod
    def sql_select_all_deep(cls):
        tbl = cls.__name__.lower()
        flds = ['%s.id' % tbl] + cls.deep_fields()
        lbls = ['AA'] + cls.deep_labels()
        qtws = ['int'] + cls.deep_widgets()
        joins = cls.deep_joins()
        sqt = "SELECT %s\nFROM %s\n%s"
        sql = sqt % (', '.join(flds), tbl, '\n'.join(joins))
        return {'sql': sql, 'labels': lbls, 'cols': flds,
                'qt_widgets_types': qtws, 'colnum': len(flds)}

    @classmethod
    def save(cls, dva):
        """Save Data dictionary dva to database

        :param dbf: Database file

        :param dva: dictionary of values"""
        if not cls.__dbf__:
            return False, 'No Database connection'
        if dva['id'] is None or dva['id'] == '':
            sqt = 'INSERT INTO %s(%s) VALUES(%s);'
            flds = ', '.join([i for i in dva.keys() if i != 'id'])
            vls = ', '.join(["'%s'" % dva[i] for i in dva.keys() if i != 'id'])
            sql = sqt % (cls.table_name(), flds, vls)
        else:
            sqt = "UPDATE %s SET %s WHERE id='%s';"
            sts = ', '.join(["%s='%s'" % (i, j) for i, j in dva.items()])
            sql = sqt % (cls.table_name(), sts, dva['id'])
        return df.save(cls.__dbf__, sql)

    @classmethod
    def validate(cls, dic_data):
        errors = []
        validated = True
        if not cls.__dbf__:
            return False, 'No Database connection'
        for fldname, fldobj in cls.field_objects().items():
            valresult, msg = fldobj.validate(dic_data[fldname])
            if not valresult:
                errors.append('%s->%s' % (fldname, msg))
                validated = False
        return validated, errors

    @classmethod
    def delete(cls, idv):
        # Delete here ...
        is_in_relation = cls.__database__.integrity(cls.table_name(), idv)
        if not is_in_relation:
            sql = "DELETE FROM %s WHERE id='%s';" % (cls.table_name(), idv)
            return df.delete(cls.__dbf__, sql)
        else:
            return False, 'Record participates in relation'

    @classmethod
    def select_all(cls):
        """Select all(To be corrected)"""
        if not cls.__dbf__:
            return False, 'No Database connection'
        sql = 'SELECT * FROM %s' % cls.__name__.lower()
        return df.read(cls.__dbf__, sql, 'cols_rows')

    @classmethod
    def select_all_deep(cls):
        """Deep select all"""
        if not cls.__dbf__:
            return False, 'No Database connection'
        metadata = cls.sql_select_all_deep()
        _, rows = df.read(cls.__dbf__, metadata['sql'], 'rows')
        metadata['rows'] = rows
        metadata['rownum'] = len(rows)
        return metadata

    @classmethod
    def search(cls, search_string):
        """Find records with many key words in search_string"""
        if not cls.__dbf__:
            return False, 'No Database connection'
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
        adic = df.read(cls.__dbf__, sql, 'cols_rows')
        return adic

    @classmethod
    def search_deep(cls, search_string):
        """Deep search

        :param dbf: Database file
        :param search_string: search string
        """
        if not cls.__dbf__:
            return False, 'No Database connection'
        search_list = search_string.split()
        meta = cls.sql_select_all_deep()
        search_field = " || ' ' || ".join(meta['cols'])
        where = ''
        search_sql = []
        for search_str in search_list:
            grup_str = gr.grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = ' WHERE '
        sql = meta['sql'] + where + ' AND '.join(search_sql)
        _, rows = df.read(cls.__dbf__, sql, 'rows')
        meta['rows'] = rows
        meta['rownum'] = len(rows)
        return meta

    @classmethod
    def search_by_id(cls, idv):
        """Search for a specific record by id

        :param dbf: Database file
        :param idv: the id to find

        :return: a dictionary with data or None (if not found)
        """
        if not cls.__dbf__:
            return False, 'No Database connection'
        sql = "SELECT * FROM %s WHERE id='%s'" % (cls.__name__, idv)
        _, record = df.read(cls.__dbf__, sql, 'one')
        return record

    @classmethod
    def search_by_id_deep(cls, idv):
        """Search for a specific record by id deep. Deep means that it returns
           actual data deep down the parent table hierarchy.

        :param dbf: Database file
        :param idv: the id to find
        :return: a dictionary with data or None (if not found)
        """
        if not cls.__dbf__:
            return False, 'No Database connection'
        data = cls.sql_select_all_deep()
        # data = cls.sql_select_ful_deep()
        sql = "%s WHERE %s.id='%s'" % (data['sql'], cls.__name__, idv)
        _, record = df.read(cls.__dbf__, sql, 'one')
        return record

    # For Deletion
    @classmethod
    def sql_select_ful_deep1(cls, field_list=None, label_list=None,
                             qt_widget_list=None, joins=None):
        """Returns sql with all relations of table

        :param dbf: Database file
        :param field_list: A list of fields (for recursion)
        :param label_list: A list of labels (for recursion)
        :param qt_widget_list: A list of qt_widgets (for recursion)
        :param joins: A list of joins (for recursion)
        """
        table_name = cls.__name__.lower()  # όνομα πίνακα σε πεζά
        flds = cls.field_names()  # [field1, field2, ...]
        fld_dic = {table_name: []}
        # Recursive variables
        field_list = field_list or ['%s.id' % table_name]  # Add id
        label_list = label_list or ['ΑΑ']  # Add label for id
        qt_widget_list = qt_widget_list or ['int']  # Add type for id
        joins = joins or []
        # End Recursive variables
        for fld in flds:
            object_fld = getattr(cls, fld)
            if object_fld.__class__.__name__ == 'ForeignKey':
                ftbl = object_fld.ftable.table_name()  # Table name of fkey
                if object_fld.null:
                    intl = 'LEFT JOIN %s ON %s.id=%s.%s'
                else:
                    intl = 'INNER JOIN %s ON %s.id=%s.%s'
                joins.append(intl % (ftbl, ftbl, table_name, fld))
                fld_dic[table_name].append(
                    object_fld.ftable.sql_select_all_deep(
                        field_list, label_list, qt_widget_list, joins))
            else:
                fld_dic[table_name].append('%s.%s' % (table_name, fld))
                field_list.append('%s.%s' % (table_name, fld))
                label_list.append(object_fld.label)
                qt_widget_list.append(object_fld.qt_widget)
        sqt = "SELECT %s\nFROM %s\n%s"
        sql = sqt % (', '.join(field_list), table_name, '\n'.join(joins))
        return {'sql': sql, 'labels': label_list, 'cols': field_list,
                'qt_widgets_types': qt_widget_list, 'colnum': len(field_list)}

    # For Deletion
    @classmethod
    def select_ful_deep1(cls):
        """Deep select all"""
        if not cls.__dbf__:
            return False, 'No Database connection'
        metadata = cls.sql_select_ful_deep()
        _, rows = df.read(cls.__dbf__, metadata['sql'], 'rows')
        metadata['rows'] = rows
        metadata['rownum'] = len(rows)
        return metadata
