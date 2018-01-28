import os.path
import sqlite3
from . import gr
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
