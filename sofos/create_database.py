import sqlite3
IGNORE = 'models'


def sql_database_create(models):
    """models: models.py from our project folder """
    classes = [cls for cls in dir(models) if (cls[0] != '_' and cls != IGNORE)]
    tsql = 'BEGIN TRANSACTION;\n\n'
    for cls in classes:
        aaa = getattr(models, cls)
        tsql += aaa.sql_create()
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
        return False, '%s\n%s' % (sql, err)
    except Exception as err:
        return False, err
    with open(filename, 'w') as fil:
        fil.write(data)
    return True, 'Database %s backup saved to %s' % (dbf, filename)
