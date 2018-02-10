import sqlite3
import os.path
from . import gr


def save(dbf, sql):
    """Safely save (create or update) data to database

    :param dbf: Database file name (full path)
    :param sql: select sql

    :return: True is operation successful, else False
    """
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    if sql.lower()[:6] not in ('insert', 'update'):
        return False, "sql does not start with insert or update"
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


def read(dbf, sql, returns):
    """SELECT

    :param dbf: Database file
    :param sql: sql
    :param returns: Return Type

    :return: one, list of dicts, cols/rows, rows
    """
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    if not sql.lower().startswith('select'):
        return False, 'sql (%s) does not start with select' % sql
    if returns not in ('one', 'list_of_dicts', 'cols_rows', 'rows'):
        msg = "returns must be one of (one, list_of_dicts, cols_rows, rows)"
        return False, msg
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
            col = tuple([t[0] for t in cur.description])
        except sqlite3.OperationalError as err:
            return False, str(err)
        if returns == 'one':
            # {'id': 1, 'key1': val1, 'key2': val2, ...}
            row = cur.fetchone()
            if row:
                return True, dict(zip([c[0] for c in cur.description], row))
            else:
                return False, {}
        elif returns == 'list_of_dicts':
            # [{'id': 1, 'k1': v1, ...}, {'id': 2, 'k1': v1, ...}]
            rows = cur.fetchall()
            ldicts = []
            for row in rows:
                ldicts.append(dict(zip([c[0] for c in cur.description], row)))
            return True, ldicts
        elif returns == 'cols_rows':
            # {'cols': (c1, c2,..),
            # 'rows': [(1, v1, ..), (2, v1, ..), ...],
            # 'rownum': 34,
            # 'colnum': 4}
            row = cur.fetchall()
            return True, {'cols': col, 'rows': row, 'rownum': len(row),
                          'colnum': len(col)}
        elif returns == 'rows':
            # [(a1, a2, ...), (b1, b2, ...), ...]
            rows = cur.fetchall()
            return True, rows


def delete(dbf, sql):
    """Delete from db

    :param dbf: Database file
    :param sql: sql

    :return: True if success, False else
    """
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    if not sql.lower().startswith('delete'):
        return False, 'sql (%s) does not start with delete' % sql
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
    cur.close()
    con.close()
    return True, 'Record deleted'


def script(dbf, sql, create=False):
    """Run sql script against database dbf

    :param dbf: Database file name(full path)
    :param sql: Sql to execute (Normally inside Transaction)
    :param create: If True creates new database file
    """
    if create:
        if os.path.isfile(dbf):
            return False, 'Database file %s already exists' % dbf
    else:
        if not os.path.isfile(dbf):
            return False, 'Database file %s does not exist' % dbf
    try:
        with sqlite3.connect(dbf) as con:
            con.executescript(sql)
    except sqlite3.Error as err:
        return False, str(err)
    return True, 'Script executed succesfuly'


def backup(dbf, backupfile, overwrite=False, inserts_only=True):
    """Backup database

    :param dbf: Database file to backup
    :param backupfile: backup destination filename
    :param overwite: If is allowed to overwrite
    :param inserts_only: If True backup data only, if False backup everything

    :return: True if backup was successful
    """
    SEL = ('INSERT INTO', 'BEGIN', 'COMMIT')

    def _insel(lin):
        """For use in backup_database"""
        for elm in SEL:
            if lin.startswith(elm):
                return True
        return False
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    if not overwrite and os.path.isfile(backupfile):
        return False, 'File %s already exists' % backupfile
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
    with open(backupfile, 'w') as fil:
        fil.write(data)
    return True, 'Database %s backup saved to %s' % (dbf, backupfile)


def ref_exists(dbf, table, field, idv):
    sql = "SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table, field, idv)
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    try:
        with sqlite3.connect(dbf) as con:
            cur = con.cursor()
            cur.execute(sql)
            row = cur.fetchone()
    except sqlite3.Error as err:
        return False, '%s\n' % err
    except Exception as err:
        return False, err
    if row[0] > 0:
        return True
    return False
