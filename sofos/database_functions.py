"""Library to acces database"""
import os.path
import sqlite3
from . import gr
import hashlib
IGNORE = 'models'
DELETE, INSERT, UPDATE = range(3)


class ValidateException(Exception):
    pass


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


def select_one(dbf, sql):
    """Run a select
        returns one dict {'id': 1, 'v1': ...}
    """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        # con.row_factory = sqlite3.Row
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
        except sqlite3.OperationalError:
            return None
        row = cur.fetchone()
        return dict(zip([c[0] for c in cur.description], row))


def select_list_of_dicts(dbf, sql):
    """Run a select
        returns [{'id': 1, 'v1': ...}, {'id': 2, 'v1':....}]
    """
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
    """Run a select
        returns {'cols': [c1, c2,..], 'rows': [[1, v1, ..], [2, v1, ..], ...]}
    """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        # con.row_factory = sqlite3.Row
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
            col = [t[0] for t in cur.description]
        except sqlite3.OperationalError:
            return None
        row = cur.fetchall()
    return {'cols': col, 'rows': row, 'rownum': len(row), 'colnum': len(col)}


def calc_md5(models):
    """models: models.py from our project folder """
    tables = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    tdic = {}
    for cls in tables:
        aaa = getattr(models, cls)
        tdic[aaa.table_name()] = aaa
    arr = []
    for key in tdic:
        arr.append(key)
        arr += tdic[key].fields()
    arr.sort()
    md5 = hashlib.md5()
    md5.update(str(arr).encode())
    return md5.hexdigest()


def create_z_table(models):
    md5 = calc_md5(models)
    sql = ("CREATE TABLE IF NOT EXISTS z ("
           "key TEXT NOT NULL PRIMARY KEY, "
           "val TEXT);\n"
           "INSERT INTO z VALUES ('md5', '%s');\n" % md5)
    return sql


def check_database_against_models(dbf, models):
    md5_from_models = calc_md5(models)
    sql = "SELECT val FROM z WHERE key='md5'"
    try:
        md5_from_db = select_one(dbf, sql)['val']
    except TypeError:
        return False
    # print(md5_from_models, md5_from_db)
    return md5_from_models == md5_from_db


def sql_database_create(models):
    """models: models.py from our project folder """
    classes = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    tsql = 'BEGIN TRANSACTION;\n\n'
    for cls in classes:
        aaa = getattr(models, cls)
        tsql += aaa.sql_create()
    tsql += create_z_table(models)
    return tsql + 'COMMIT;'


def create_tables(dbf, models, print_only=False):
    sql = sql_database_create(models)
    # print('Database file: %s' % dbf)
    # print(sql)
    if print_only:
        return True
    try:
        with sqlite3.connect(dbf) as con:
            con.executescript(sql)
    except sqlite3.Error as err:
        return False, '%s\n%s' % (sql, err)
    except Exception as err:
        return False, err
    return True, 'Database file %s created !!' % dbf


def insel(lin):
    SEL = ('INSERT INTO', 'BEGIN', 'COMMIT')
    for elm in SEL:
        if lin.startswith(elm):
            return True
    return False


def backup_database(dbf, filename):
    try:
        with sqlite3.connect(dbf) as con:
            data = '\n'.join([i for i in con.iterdump() if insel(i)])
    except sqlite3.Error as err:
        return False, '%s\n' % err
    except Exception as err:
        return False, err
    with open(filename, 'w') as fil:
        fil.write(data)
    return True, 'Database %s backup saved to %s' % (dbf, filename)
