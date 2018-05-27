"""Module Database"""
import os
import datetime
import hashlib
from . import dbf as dbi
IGNORE = 'models'


class Database():
    """Database Class"""

    def __init__(self, models, dbf=None):
        """Initialize

        :param models: user models module
        :param dbf: database file
        """
        self.models = models
        self.dbf = dbf if self.set_database(dbf) else None

    @property
    def is_connected(self):
        return True if self.dbf else False

    def integrity_dict(self):
        """Integrity dictionary

        :return: Dictionary {parent1: {child1: fld1, child2: fld2, ...}, ...}
        """
        in_dic = {}
        for table_name, table_object in self.table_objects().items():
            for fld_name, fld_obj in table_object.field_objects().items():
                if fld_obj.fkey:
                    parent = fld_obj.ftable.table_name()
                    child = table_name
                    field = fld_name
                    in_dic[parent] = in_dic.get(parent, {})
                    in_dic[parent][child] = field
        return in_dic

    def integrity(self, parent_table, id_value):
        idict = self.integrity_dict()
        if parent_table not in idict:
            return False
        else:
            for child, field in idict[parent_table].items():
                if dbi.ref_exists(self.dbf, child, field, id_value):
                    return True
        return False

    def set_database(self, dbf):
        """Set database if compatible

        :param dbf: Database file name

        :return: True or False.
        """
        if not dbf:
            return False
        if self.is_database_compatible(dbf):
            self.dbf = dbf
            return True
        return False

    def create_database(self, dbf, init_db_file=None):
        """Create tables from model definitions

        :param dbf: Database filename
        :param models: The models module to use (Normally models.py in your
            application's root)
        :param init_db_file: The init_db_file.sql file to use if present
        """
        msg = ''
        success, info = dbi.script(
            dbf, self.sql_database_create(), create=True)
        if not success:
            return success, info
        else:
            self.dbf = dbf
            msg = 'Database %s created successfuly' % (dbf)
        success2, info2 = True, ''
        if init_db_file and os.path.isfile(init_db_file):
            with open(init_db_file) as file:
                success2, info2 = dbi.script(dbf, file.read())
            if success2:
                msg += '\ninitial data inserted successfuly'
            else:
                msg += '\nproblem inserting initial data'
        return success, msg

    def sql_database_create(self):
        """Create sql for table creation according to your model settings

        :param models: normally models.py from your project folder

        :return: create sql
        """
        classes = [cls for cls in dir(self.models)
                   if (cls[0] != '_' and cls != IGNORE)]
        tsql = 'BEGIN TRANSACTION;\n\n'
        for cls in classes:
            aaa = getattr(self.models, cls)
            tsql += aaa.sql_create()
        tsql += self.create_z_table()
        return tsql + 'COMMIT;'

    def backup_database(self):
        """Backup database with timestamp"""
        timestamp = datetime.datetime.now().isoformat()
        tsr = timestamp.replace('-', '').replace('T', '').replace(':', '')[:12]
        filename = '%s.%s.sql' % (self.dbf, tsr)
        if self.dbf:
            return dbi.backup(
                self.dbf, filename, overwrite=True, inserts_only=True)
        else:
            return False, 'Error during backup procedure'

    def restore_database(self):
        """Not implemented yet"""
        return False, 'Not Implemented yet'

    def table_objects(self):
        """models: models.py from our project folder

        :return: Dictionary

        return dictionary format::

            {table_name1: table_object1, ...}
        """
        tables = [tbl for tbl in dir(self.models)
                  if (tbl[0] != '_' and tbl != IGNORE)]
        table_dict = {}
        for tbl in tables:
            model = getattr(self.models, tbl)
            table_object = getattr(self.models, tbl)
            # injecting database file name to table model here
            table_object.__dbf__ = self.dbf
            table_object.__database__ = self
            table_dict[model.table_name()] = table_object
        return table_dict

    def table_object(self, table_name):
        """Returns table object by table name

        :param table_name: table name
        """
        tableobject = self.table_objects().get(table_name, None)
        return tableobject

    def table_names(self):
        """Returns table names"""
        tnames = []
        for table_object in self.table_objects():
            tnames.append(table_object)
        return tnames

    def table_labels(self, as_dict=False):
        """Returns table labels"""
        tlabels = {} if as_dict else []
        for tname, tobject in self.table_objects().items():
            if as_dict:
                tlabels[tname] = tobject.table_label()
            else:
                tlabels.append(tobject.table_label())
        return tlabels

    def is_database_compatible(self, dbf):
        """This function checks the databases creation md5 against current
        models md5 in order to evaluate equality of the two schemas

        :param dbf: Database file
        :param models: normally models.py from your project folder

        :return: True if database schema is the same with model schema
        """
        md5_from_models = self.calc_md5()
        sql = "SELECT val FROM z WHERE key='md5'"
        try:
            success, md5_dict = dbi.read(dbf, sql, 'one')
        except TypeError:
            return False
        if success:
            return md5_from_models == md5_dict['val']
        else:
            return False

    def calc_md5(self):
        """Calculates the md5 of the models schema

        :param models: normally models.py from your project folder

        :return: md5 value
        """
        tables = [cls for cls in dir(self.models)
                  if (cls[0] != '_' and cls != IGNORE)]
        tdic = {}
        for cls in tables:
            aaa = getattr(self.models, cls)
            tdic[aaa.table_name()] = aaa
        arr = []
        for key in tdic:
            arr.append(key)
            arr += tdic[key].field_names()
        arr.sort()
        md5 = hashlib.md5()
        md5.update(str(arr).encode())
        return md5.hexdigest()

    def create_z_table(self):
        """Create a metadata keys/values table and insert at least the md5 of the
           models schema.

        :param models: normally models.py from your project folder
        """
        md5 = self.calc_md5()
        sql = ("CREATE TABLE IF NOT EXISTS z ("
               "key TEXT NOT NULL PRIMARY KEY, "
               "val TEXT);\n"
               "INSERT INTO z VALUES ('md5', '%s');\n" % md5)
        return sql
