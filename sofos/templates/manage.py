#!/usr/bin/env python
import sys
import models as mb
from sofos import database_functions as cd


if __name__ == '__main__':
    # command = sys.argv[1]
    argsize = len(sys.argv)
    if argsize == 1:
        pass
    elif argsize >= 2:
        command = sys.argv[1]
        assert command in ('run', 'dbcreate')
        if command == 'dbcreate':
            if argsize >= 3:
                dbname = sys.argv[2]
            else:
                dbname = 'testdb.sqlite3'
            cd.create_tables(dbname, mb)
        elif command == 'run':
            from main import run
            run()
