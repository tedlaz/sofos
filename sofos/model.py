"""Model"""
import os.path
import sqlite3
from . import gr
DELETE, INSERT, UPDATE = range(3)


class ValidateException(Exception):
    pass


def sql_cud(table, data, typ=INSERT):
    """flds, vals are tuples"""
    flds = []
    vals = []
    for fld in data:
        flds.append(fld)
        if data[fld] == '' and fld == 'id':
            vals.append('null')
        else:
            vals.append("'%s'" % data[fld])
    if typ == INSERT:
        sqlinsert = "INSERT INTO %s (%s) VALUES (%s)"
        sql = sqlinsert % (table, ', '.join(flds), ', '.join(vals))
        return sql
    elif typ == UPDATE:
        sqlupdate = "UPDATE %s SET %s WHERE id=%s"
        qms = ["%s='%s'" % (fld, data[fld]) for fld in data if fld != 'id']
        sql = sqlupdate % (table, ', '.join(qms), data['id'])
        return sql
    elif typ == DELETE:
        sql = "DELETE FROM %s WHERE id=%s" % (table, data['id'])
        return sql
    return None


def field_lbl(dbf, name):
    """Run a select """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT slbl FROM zfl WHERE sfld='%s'" % name)
        except sqlite3.OperationalError:
            return name
        rows = cur.fetchone()
    return rows[0] if rows else name


def table_lbl(dbf, name):
    """Run a select """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        try:
            cur.execute("SELECT snam FROM zt WHERE stbl='%s'" % name)
        except sqlite3.OperationalError:
            return name
        rows = cur.fetchone()
    return rows[0] if rows else name


def table_fields(dbf, tablename):
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        try:
            cur.execute("select * from %s limit(0)" % tablename)
            column_names = [t[0] for t in cur.description]
        except sqlite3.OperationalError:
            return None
    return column_names


def table_metadata(dbf, table_name):
    columns = table_fields(dbf, table_name)
    tlbl = table_lbl(dbf, table_name)
    clbl = {}
    clbld = []
    for col in columns:
        clbl[col] = field_lbl(dbf, col)
        clbld.append(clbl[col])
    return {'table': table_name, 'tablelbl': tlbl,
            'cols': columns, 'colslbl': clbl, 'colslbld': clbld }


def table_rpr(dbf, table, idv):
        sql1 = "SELECT * FROM %s_rpr WHERE id=%s" % (table, idv)
        sql2 = "SELECT * FROM %s WHERE id=%s" % (table, idv)
        val = select(dbf, sql1)
        if val:
            return val[0]['rpr']
        val = select(dbf, sql2)
        rep = []
        if val:
            for key in val[0]:
                if key != 'id':
                    if key.endswith('_id') or key.endswith('_cd'):
                        rep.append(table_rpr(dbf, key[:-3], val[0][key]))
                    else:
                        rep.append(str(val[0][key]))
        else:
            return idv
        final = ' '.join(rep)
        return final[:30]


def cud(dbf, sql):
    """Safely save data to database"""
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except sqlite3.Error as err:
        con.rollback()
        cur.close()
        con.close()
        return False, str(err)
    last_inserted_id = cur.lastrowid
    cur.close()
    con.close()
    return True, last_inserted_id


def select(dbf, sql):
    """Run a select """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        # con.row_factory = sqlite3.Row
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
        except sqlite3.OperationalError:
            return None
        rows = cur.fetchall()
        ldicts = []
        for row in rows:
            ldicts.append(dict(zip([c[0] for c in cur.description], row)))
    return ldicts


def select_cols_rows(dbf, sql):
    """Run a select """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        # con.row_factory = sqlite3.Row
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
            column_names = [t[0] for t in cur.description]
        except sqlite3.OperationalError:
            return None
        rows = cur.fetchall()
    return {'cols': column_names, 'rows': rows}


class Model():
    def __init__(self, dbf, table):
        if not os.path.isfile(dbf):
            raise FileNotFoundError("File %s doesn't exist" % dbf)
        self._dbf = dbf
        self._table = table
        self._fields = self._fields_from_db()

    @property
    def dbf(self):
        return self._dbf

    @property
    def table(self):
        return self._table

    @property
    def fields(self):
        return self._fields

    @property
    def metadata(self):
        return table_metadata(self._dbf, self._table)

    def _fields_from_db(self):
        """Get"""
        sql = 'SELECT * FROM %s LIMIT 0' % self._table
        with sqlite3.connect(self._dbf) as con:
            cur = con.cursor()
            cur.execute(sql)
            column_names = [t[0] for t in cur.description]
            cur.close()
        assert 'id' in column_names
        return tuple(column_names)

    @property
    def select_all(self):
        sql = 'SELECT * FROM %s' % self._table
        return select(self._dbf, sql)

    @property
    def select_all_cols_rows(self):
        sql = 'SELECT * FROM %s' % self._table
        adic = select_cols_rows(self._dbf, sql)
        adic['table'] = self._table
        adic['dbf'] = self._dbf
        adic['colnum'] = len(adic['cols'])
        adic['rownum'] = len(adic['rows'])
        return adic

    def search(self, search_string):
        """Find records with many key words in search_string"""
        search_list = search_string.split()
        search_sql = []
        search_field = " || ' ' || ".join(self._fields)
        sql1 = "SELECT * FROM %s \n" % self._table
        where = ''
        for search_str in search_list:
            grup_str = gr.grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = 'WHERE'
        # if not search_string sql is simple select
        sql = sql1 + where + ' AND '.join(search_sql)
        adic = select_cols_rows(self._dbf, sql)
        adic['table'] = self._table
        adic['dbf'] = self._dbf
        adic['colnum'] = len(adic['cols'])
        adic['rownum'] = len(adic['rows'])
        return adic

    def search_by_id(self, idv):
        """Returns dictionary with unique by id data or None"""
        sql = "SELECT * FROM %s WHERE id=%s" % (self._table, idv)
        val = select(self._dbf, sql)
        if val:
            return val[0]
        else:
            return None

    def rpr(self, idv):
        return table_rpr(self.dbf, self.table, idv)

    def save(self, data):
        """code to save or update here"""
        if not self._validate(data):
            return
        if data['id'] == '':
            # Do insert
            val = cud(self._dbf, sql_cud(self._table, data, INSERT))
        else:
            # Do update
            val = cud(self._dbf, sql_cud(self._table, data, UPDATE))
        return val

    def _validate(self, data):
        """validate values"""
        # raise ValidateException('Data not validated')
        for field in self._fields:
            if field not in data:  # all fields must be present
                raise ValidateException('Missing field %s' % field)
        return True
