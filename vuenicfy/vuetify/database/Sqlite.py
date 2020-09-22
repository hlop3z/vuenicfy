import sqlite3

class SQLiteORM:
    def __init__(self, name=None, conn=None, tx=None):
        self.name  = name
        self.conn  = conn
        self.tx    = tx

    def create_table(self, fields):
        try:
            data = self.tx.execute( f'''CREATE TABLE { self.name }({ fields });''' )
        except:
            data = False
        return data


    def records(self, by=None):
        try:
            recs = self.tx.execute( f'''SELECT * FROM { self.name };''' )
            if by: data = {  r[ by ]: r  for r in recs }
            else : data = [ r for r in recs ]
        except:
            data = False
        return data


    def create(self, **kwargs):
        try:
            fields  = ",".join( kwargs.keys() )
            _fields = ",".join( [ '?' for k in kwargs.keys() ] )
            data    = self.tx.execute( f'''INSERT INTO { self.name }({ fields }) VALUES ({ _fields });''', (*kwargs.values(),) )
            self.conn.commit()
            data    = True
        except:
            data    = False
        return data


    def update(self, __query__={}, **kwargs):
        try:
            _form   = ",".join( [ f'''{ k }=?''' for k in __query__.keys() ] )
            _fields = ",".join( [ f'''{ k }=?''' for k in kwargs.keys() ] )
            data    = self.tx.execute( f'''UPDATE { self.name } SET { _fields } WHERE { _form };''', (*kwargs.values(),*__query__.values(),) )
            self.conn.commit()
            data    = True
        except:
            data    = False
        return data


    def delete(self, **kwargs):
        try:
            _fields = ",".join( [ f'''{ k }=?''' for k in kwargs.keys() ] )
            data    = self.tx.execute( f'''DELETE FROM { self.name } WHERE { _fields };''', (*kwargs.values(),) )
            self.conn.commit()
            data    = True
        except:
            data    = False
        return data


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Sqlite:
    def __init__(self, name=':memory:'):
        connection = sqlite3.connect( name )
        cursor     = connection.cursor()

        connection.row_factory = dict_factory

        self.conn  = connection
        self.tx    = connection.cursor()
        self.tables= connection.cursor()

    def Model(self, name=None):
            return SQLiteORM(name=name, conn=self.conn, tx=self.tx)
