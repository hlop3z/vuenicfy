from collections import namedtuple
import inspect

from . import register_plugin
from .sqlow import Sqlow
from .schema import Schema

PLUGINS  = dict()
RESPONSE = namedtuple('Schemas', ['error', 'data', 'method'])

class SchemaBase:
    def __init__(self, name=None, schema=None, sqlite=False):
        self.name      = name
        self.form      = Schema( **schema )
        self.sql       = Sqlow( name, sqlite = sqlite )

        def create( form=None ):
            create = self.form.create( form )
            if not create.error: return RESPONSE(False, self.sql.create( create.data ), 'sql-create')
            return create

        def read( query=None, fields=['*'] ):
            return RESPONSE(False, self.sql.find( query, fields ), 'sql-where')

        def update( form=None, query=None ):
            update = self.form.update( form )
            if not update.error: return RESPONSE(False, self.sql.update( update.data, query ), 'sql-update')
            return update

        def delete( query=None ):
            return RESPONSE(False, self.sql.delete( query ), 'sql-delete')

        self.route( create )
        self.route( update )
        self.route( delete )
        self.route( read )


    def route(cls, function):
        # Set-Name
        bp_name = f'''{ cls.name.lower() }'''
        name    = function.__name__
        # Set-SchemaBase
        if not bp_name in PLUGINS: PLUGINS[ bp_name ] = { "info": cls.form.info._asdict() }
        # Register Function
        if name in PLUGINS[ bp_name ]: raise Exception(f'''Function: < { name } > inside Schema: < { bp_name } > is Already Registered!''')
        else                         : PLUGINS[ bp_name ][ name ] = function



@register_plugin
class Schemas:
    '''
create({ "form": {} })
read({ "query": {}, "fields": [] })
update({ "form": {}, "query": {} })
delete({ "query": {} })
    '''
    def __init__(self, schemas=[], sqlite=False):
        for s in schemas: s['sqlite'] = sqlite
        self.info = { }
        for s in schemas:
            SchemaBase( **s )
            self.info[ s['name'] ] = dict(PLUGINS[ s['name'] ]['info'])

    @property
    def methods(self): return PLUGINS

    @property
    def keys(self): return list( self.info.keys() )
