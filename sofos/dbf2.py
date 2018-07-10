import os.path
import sqlite3


def sql_insert(table, adic, fkey_field=None):
    sqt = 'INSERT INTO {tbl} ({flds}) VALUES ({vals});'
    fls = ', '.join([i for i in adic.keys() if i != 'id'])
    val = []
    for key, value in adic.items():
        if key == 'id':
            continue
        elif key == fkey_field:
            val.append("'{idv}'")
        else:
            val.append("'%s'" % value)
    return sqt.format(tbl=table, flds=fls, vals=', '.join(val))


def sql_update(table, adic, fkey_field=None):
    sqt = "UPDATE %s set {flds} WHERE id='%s';" % (table, adic['id'])
    fls = []
    for key, val in adic.items():
        if key == 'id':
            continue
        if key == fkey_field:
            fls.append("%s='{idv}'" % key)
        else:
            fls.append("%s='%s'" % (key, val))
    # fls = ', '.join(["%s='%s'" % (k, v)for k, v in adic.items() if k != 'id'])
    return sqt.format(flds=', '.join(fls))


def sql_save(table, adic, key=None):
    idv = adic.get('id', '')
    if idv == '':
        return sql_insert(table, adic, key)
    return sql_update(table, adic, key)


def sql_delete(table, field, idv):
    return "DELETE FROM %s WHERE %s='%s';" % (table, field, idv)


def sql_transaction(sql_list):
    return 'BEGIN;\n' + '\n'.join(sql_list) + '\nCOMMIT;'


def sql_save_one2many(ddi):
    master = ddi.get('master', None)
    key = ddi.get('key', None)
    # Πρέπει πάντα να υπάρχει τιμή για το table-master
    assert master
    # Πρέπει ή και τα δύο ή κανένα από τα δύο
    detail = ddi.get('detail', None)
    if detail or key:
        assert detail and key
    # Ολοκληρωτική διαγραφή με βάση το id
    del_key = ddi.get('delete-master-id', None)
    if del_key:
        sqm = sql_delete(master, 'id', del_key)
        sqd = sql_delete(detail, key, del_key)
        return '', sqm, [sqd, ], []
    dmaster = ddi.get('dmaster', {})
    sqm = sql_save(master, dmaster)
    ddetail = ddi.get('ddetail', {})
    sqd = [sql_save(detail, i, key) for i in ddetail]
    idv = dmaster.get('id', '')
    del_dkeys = ddi.get('delete-detail-ids', [])
    sqdel = [sql_delete(detail, 'id', idv) for idv in del_dkeys]
    return idv, sqm, sqd, sqdel


def save_one2many(dbf, idv, sqm, sqd, sqdel):
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        cur.execute(sqm)
        key = idv or cur.lastrowid
        for sqt in sqd:
            cur.execute(sqt.format(idv=key))
        for sql in sqdel:
            cur.execute(sql)
        con.commit()


def save(dbf, datadict):
    """
    :param dbf: Database file path
    :param datadict: dictionary with keys
        master  : Master table name.
        detail  : Detail table name.
        key     : field of detail foreign key to master.
        dmaster : Dictionary with master record data.
        ddetail : List of dictionaries with detail records.
        del-id  : If present delete all with this id.
        ddel-ids: List of detail ids to delete.
    """
    idv, sqm, sqd, sqdel = sql_save_one2many(datadict)
    save_one2many(dbf, idv, sqm, sqd, sqdel)


def sel(dbf, master, detail, key, idv):
    sqt = 'SELECT * FROM %s WHERE %s=%s'
    sqm = sqt % (master, 'id', idv)
    sqd = sqt % (detail, key, idv)
    fdi = {'master': master, 'detail': detail, 'key': key}
    with sqlite3.connect(dbf) as con:
        try:
            cur = con.cursor()
            cur.execute(sqm)
            rowm = cur.fetchone()
            dmaster = dict(zip([c[0] for c in cur.description], rowm))
            cur.execute(sqd)
            rows = cur.fetchall()
            dd = [dict(zip([c[0] for c in cur.description], r)) for r in rows]
        except Exception as err:
            fdi['dmaster'] = {}
            fdi['ddetail'] = []
            fdi['error'] = err
            return fdi
    fdi['dmaster'] = dmaster
    fdi['ddetail'] = dd
    return fdi


if __name__ == '__main__':
    dbf = '/home/ted/devtest/ted1/tst.sql3'
    dff = {'master': 'tran',
           'detail': 'trand',
           'key': 'tran',
           'delete-master-id': 5,
           'dmaster': {'id': '', 'par': 'TIM689', 'per': 'Αγορές γενικά'},
           'ddetail': [{'id': '', 'tran': '', 'lmo': '20', 'xr': 5, 'pi': 0},
                       {'id': '', 'tran': '', 'lmo': '54', 'xr': 2, 'pi': 0},
                       {'id': '', 'tran': '', 'lmo': '50', 'xr': 0, 'pi': 7},
                       ],
           'delete-detail-ids': [5, 6]
           }
    # save(dbf, dff)
    print(sql_insert('pel', {'epo': 'Ted', 'ono': 'Lazaros'}))
    print(sql_update('pel', {'id': 1, 'epo': 'Tedd', 'ono': 'Lazarof'}))
    print(sql_delete('pel', 'id', 1))
    print(sel(dbf, 'tran', 'trand', 'tran', '3'))
