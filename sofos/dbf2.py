import os.path
import sqlite3
# from . import gr


def _sql_safe(data):
    """
    {'typ': 'insert', 'table': 'erg',
     'fields': {'epo': 'Lazaros', 'ono': }}
    """
    sql = ''
    vls = []
    if data['typ'] == 'insert':
        sqt = 'INSERT INTO {tbl} ({flds}) VALUES ({vals});'
        fls = ', '.join([f for f in data['fields'].keys()])
        val = ', '.join(['?' for f in data['fields'].values()])
        sql = sqt.format(tbl=data['table'], flds=fls, vals=val)
        vls = [f for f in data['fields'].values()]
    elif data['typ'] == 'update':
        assert 'id' in data['fields'].keys()
        sqt = "UPDATE {tbl} set {flds} WHERE id=?;"
        fls = ', '.join(["%s=?" % k for k, v in
                         data['fields'].items() if k != 'id'])
        sql = sqt.format(tbl=data['table'],
                         flds=fls,
                         id=data['fields']['id'])
        vls = [v for k, v in data['fields'].items() if k != 'id']
        vls.append(data['fields']['id'])
    elif data['typ'] == 'delete':
        assert 'id' in data['fields'].keys()
        sqt = "DELETE FROM {tbl} WHERE id=?;"
        sql = sqt.format(tbl=data['table'])
        vls = [data['fields']['id']]
    print(sql, tuple(vls))
    return sql, tuple(vls)


def save(dbf, datadic):
    sql, vals = _sql_safe(datadic)
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        cur.execute(sql, vals)
        return cur.lastrowid


def save_one2many(dbf, datadic):
    one = datadic['one']
    many = datadic['many']
    fkey = datadic['fkey']
    sql, vals = _sql_safe(one)
    if not os.path.isfile(dbf):
        return False, 'File %s does not exist' % dbf
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        cur.execute(sql, vals)
        key = cur.lastrowid
        if key == 0:
            key = one['fields']['id']
        for lin in many:
            if one['typ'] == 'delete':
                lin['typ'] = 'delete'
            lin['fields'][fkey] = key
            sql, vals = _sql_safe(lin)
            cur.execute(sql, vals)
        con.commit()


if __name__ == '__main__':
    dbf = '/home/ted/devtest/tst'
    ddi = {'typ': 'insert', 'table': 'erg',
           'fields': {'epo': 'Laz', 'ono': 'Ted'}}
    ddb = {'typ': 'master-detail', 'master': 'tr', 'detail': 'trd'}
    print(save(dbf, ddi))
    ddi['typ'] = 'update'
    ddi['fields']['id'] = 2
    ddi['fields']['epo'] = 'Dazea'
    print(save(dbf, ddi))
    ddi['fields']['id'] = 3
    ddi['typ'] = 'delete'
    print(save(dbf, ddi))
    fff = {'one': {'typ': 'delete', 'table': 'tr',
                   'fields': {'id': 1, 'date': '2018-01-01', 'par': 'tim112'}},
           'many': [{'typ': 'update', 'table': 'trd',
                     'fields': {'id': 1, 'tr': '', 'poso': 100}},
                    {'typ': 'insert', 'table': 'trd',
                     'fields': {'id': 5, 'poso': 888}}
                    ],
           'fkey': 'tr'}
    save_one2many(dbf, fff)
