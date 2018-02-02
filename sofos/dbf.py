"""Library with database functions"""
import os.path
import sqlite3
import hashlib
from . import gr
IGNORE = 'models'
DELETE, INSERT, UPDATE = range(3)


class ValidateException(Exception):
    pass


def cud(dbf, sql):
    """Safely save (insert or update) data to database

    :param dbf: Database file
    :parma sql: select sql
    :return: True is operation successful, else False
    """
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
    """Run a select against dbf and get one dictionary or None

    :param dbf: Database file
    :parma sql: select sql
    :return: dictionary

    Return format::

        {'id': 1, 'key1': val1, 'key2': val2, ...}
    """
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
        except sqlite3.OperationalError:
            return None
        row = cur.fetchone()
        return dict(zip([c[0] for c in cur.description], row))


def select_list_of_dicts(dbf, sql):
    """Run a select agains dbf and get a list of dictionaries

    :param dbf: Database file
    :param sql: select sql
    :return: list of dictionaries

    Return format::

        [{'id': 1, 'k1': v1, ...}, {'id': 2, 'k1': v1, ...}]
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
    """Run a select against dbf and get a dictionary

    :param dbf: Database file
    :param sql: select sql
    :return: dictionary

    Return Dictionary format::

        {'cols': [c1, c2,..],
         'rows': [[1, v1, ..], [2, v1, ..], ...],
         'rownum': 34,
         'colnum': 4}
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


def select_rows(dbf, sql):
    """Run a select against dbf

    :param dbf: Database file
    :param sql: select sql
    :return: list of tuples of values

    Return format::

        ([(1, v11, ..), (2, v12, ..), ..., (n, v1n, ..)])
    """
    rows = []
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
        except sqlite3.OperationalError as err:
            return None, err, sql
        rows = cur.fetchall()
    return rows


def calc_md5(models):
    """Calculates the md5 of the models schema

    :param models: normally models.py from your project folder
    :return: md5 value
    """
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
    """Create a metadata keys/values table and insert at least the md5 of the
       models schema.

    :param models: normally models.py from your project folder
    """
    md5 = calc_md5(models)
    sql = ("CREATE TABLE IF NOT EXISTS z ("
           "key TEXT NOT NULL PRIMARY KEY, "
           "val TEXT);\n"
           "INSERT INTO z VALUES ('md5', '%s');\n" % md5)
    return sql


def check_database_against_models(dbf, models):
    """This function checks the databases creation md5 against current models
    md5 in order to evaluate if the two schemas are the same

    :param dbf: Database file
    :param models: normally models.py from your project folder
    :return: True if database schema is the same with model schema
    """
    md5_from_models = calc_md5(models)
    sql = "SELECT val FROM z WHERE key='md5'"
    try:
        md5_from_db = select_one(dbf, sql)['val']
    except TypeError:
        return False
    # print(md5_from_models, md5_from_db)
    return md5_from_models == md5_from_db


def sql_database_create(models):
    """Create sql for table creation according to your model settings

    :param models: normally models.py from your project folder
    :return: create sql
    """
    classes = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    tsql = 'BEGIN TRANSACTION;\n\n'
    for cls in classes:
        aaa = getattr(models, cls)
        tsql += aaa.sql_create()
    tsql += create_z_table(models)
    return tsql + 'COMMIT;'


def create_tables(dbf, models, init_db=None, print_only=False):
    """Create tables from model definitions

    :param dbf: Database filename
    :param models: The models module to use (Normally models.py in your
        application's root)
    :param init_db: The init_db.sql file to use if present
    :param print_only: If True does nothing, just returns sql
    """
    sql = sql_database_create(models)
    if print_only:
        return sql
    try:
        with sqlite3.connect(dbf) as con:
            con.executescript(sql)
            if init_db and os.path.isfile(init_db):
                with open(init_db) as file:
                    con.executescript(file.read())
    except sqlite3.Error as err:
        print(sql)
        return False, str(err)
    except Exception as err:
        return False, err
    return True, 'Database file %s created !!' % dbf


def _insel(lin):
    """For use in backup_database"""
    SEL = ('INSERT INTO', 'BEGIN', 'COMMIT')
    for elm in SEL:
        if lin.startswith(elm):
            return True
    return False


def backup_database(dbf, filename, inserts_only=True):
    """Backup database

    :param dbf: Database file to backup
    :param filename: backup destination filename
    :param inserts_only: If True backup data only, if False backup everything
    :return: True if backup was successful
    """
    try:
        with sqlite3.connect(dbf) as con:
            if inserts_only:
                data = '\n'.join([i for i in con.iterdump() if _insel(i)])
            else:
                data = '\n'.join(con.iterdump())
    except sqlite3.Error as err:
        return False, '%s\n' % err
    except Exception as err:
        return False, err
    with open(filename, 'w') as fil:
        fil.write(data)
    return True, 'Database %s backup saved to %s' % (dbf, filename)
