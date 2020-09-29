import collections, sqlite3

RESPONSE = collections.namedtuple('SQLite', ['error', 'data', 'method'])

from . import register_plugin

@register_plugin
class Sqlitemin:
    """docstring for Sqlite"""
    def __init__(self, name='example.db'):
        engine             = sqlite3.connect( name )
        dict_factory       = lambda cursor, row: { col[0] : row[idx] for idx, col in enumerate(cursor.description) }
        engine.row_factory = dict_factory
        self.engine = engine


    def close( self, *args ):
        try   : self.engine.close()
        except: pass


    async def fetch( self, *args ):
        db = self.engine
        try:
            with db:
                c  = db.cursor()
                c.execute( *args )
                return RESPONSE(False, c.fetchall(), 'fetch')
        except Exception as e:
            return RESPONSE(True, e.args, 'fetch')



    async def fetchrow( self, *args ):
        db = self.engine
        try:
            with db:
                c  = db.cursor()
                c.execute( *args )
                return RESPONSE(False, c.fetchone(), 'fetch-row')
        except Exception as e:
            print( e )
            return RESPONSE(True, e.args, 'fetch-row')



    async def execute( self, *args ):
        db = self.engine
        try:
            with db:
                c  = db.cursor()
                r  = c.execute( *args )
                return RESPONSE(False, r, 'execute')
        except Exception as e:
            return RESPONSE(True, e.args, 'execute')



    async def executemany( self, *args ):
        db = self.engine
        try:
            with db:
                c  = db.cursor()
                r  = c.executemany( *args )
                return RESPONSE(False, r, 'execute-many')
        except Exception as e:
            return RESPONSE(True, e.args, 'execute-many')
