import functools, inspect, collections

from . import register_plugin
from .schemas import Schemas

PLUGINS = dict()

RESPONSE = collections.namedtuple('Blueprints', ['schemas', 'find', 'custom'])

def bp_group(*args):
    for bp in args: PLUGINS.update( bp.methods )
    return PLUGINS

class BlueprintBase:
    def __init__(self, name=None):
        self.name = name

    @property
    def methods(self): return PLUGINS

    @property
    def keys(self): return list( PLUGINS.keys() )

    def route(cls, function):
        #Set-Name
        bp_name = f'''{ cls.name.lower() }'''
        name    = function.__name__
        url     = f'''{ bp_name }/{ name }'''
        if url in PLUGINS: raise Exception(f'''{ url } - Already Registered!''')
        #Wrapped Functions
        isAsync = inspect.iscoroutinefunction( function )
        def       sync_method(*args, **kwargs) : return       function(*args, **kwargs)
        async def async_method(*args, **kwargs): return await function(*args, **kwargs)
        #Register Function
        if isAsync: PLUGINS[ url ] = async_method
        else      : PLUGINS[ url ] = sync_method

    @staticmethod
    def group(*args):
        for bp in args: PLUGINS.update( bp.methods )
        return PLUGINS


@register_plugin
def Blueprints(_schemas, sqlite = False):
    Sqlow       = Schemas(_schemas, sqlite = sqlite)
    Bps         = { s['name'] : BlueprintBase( s['name'] ) for s in _schemas }
    CustomBPs   = bp_group( *PLUGINS.values() )
    return RESPONSE(Sqlow, Bps, CustomBPs)
