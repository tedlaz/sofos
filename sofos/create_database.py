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
    print('Database file: %s' % dbf)
    print(sql)
    if print_only:
        return True
    try:
        with sqlite3.connect(dbf) as con:
            con.executescript(sql)
    except Exception:
        return False
    return True
