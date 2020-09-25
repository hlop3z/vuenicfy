from collections import namedtuple
import inspect

from . import register_plugin
from .sqlow import Sqlow
from .schema import Schema

PLUGINS = dict()

RESPONSE = namedtuple('Blueprints', ['error', 'data', 'method'])

@register_plugin
class Blueprint:
    def __init__(self, name=None, schema=None, sqlite=False):
        self.name      = name
        self.form      = Schema( **schema )
        self.sql       = Sqlow( name, sqlite = sqlite )

        def create( form=None ):
            create = self.form.create( form )
            if not create.error: return RESPONSE(False, self.sql.create( create.data ), 'sql-create')
            return create

        def update( form=None, query=None ):
            update = self.form.update( form )
            if not update.error: return RESPONSE(False, self.sql.update( update.data, query ), 'sql-update')
            return update

        def delete( query=None ):
            return RESPONSE(False, self.sql.delete( query ), 'sql-delete')

        def find( query=None, fields=['*'] ):
            return RESPONSE(False, self.sql.find( query, fields ), 'sql-where')

        self.route( create )
        self.route( update )
        self.route( delete )
        self.route( find )


    @property
    def method(self): return PLUGINS

    @property
    def urls(self): return list(PLUGINS.keys())

    def route(cls, function):
        global PLUGINS
        #Set-Name
        clsn = cls.name.lower()
        name = f'''{ clsn }/{ function.__name__ }'''
        if name in PLUGINS: raise Exception(f'''{ name } - Already Registered!''')

        #Fake Functions
        isAsync = inspect.iscoroutinefunction( function )
        def       sync_method(*args, **kwargs) : return       function(*args, **kwargs)
        async def async_method(*args, **kwargs): return await function(*args, **kwargs)

        #Register Function
        if isAsync: PLUGINS[ name ] = async_method
        else      : PLUGINS[ name ] = sync_method
