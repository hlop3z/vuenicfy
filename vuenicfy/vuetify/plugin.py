import functools, pathlib, json

from . import register_plugin, frontend, backend

APP_PATH    = pathlib.Path(__file__).resolve().parents[2]

with open(f"{ APP_PATH }/CONFIG.json", "r") as f:
    CONFIG = json.load(f)

component = frontend.Model('components')
component.create_table('''
    name text primary key,
    data text,
    metadata text
''')

@register_plugin
def create():
    data = component.create(name='testing')
    return data

@register_plugin
def records():
    data = component.records()
    return data

@register_plugin
def update():
    data = component.update(__query__={ "name": "testing" }, data=None)
    return data

@register_plugin
def delete():
    data = component.delete( name='toxic' )
    return data

@register_plugin
def decorator(arg1=None, arg2=None):
    def real_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            name = function.__name__
            results = function(*args, **kwargs)
            return results
        return wrapper
    return real_decorator


PLUGINS = dict()

@register_plugin
class Blueprint:
    def __init__(self, name=None):
        self.name = name
        self.blueprints = type(name, (), {})

    @property
    def plugins(self): return PLUGINS

    @property
    def urls(self): return list(PLUGINS.keys())

    def route(cls, fields=[], arg1=None):
        def real_decorator(function):
            name = function.__name__
            bp_name = f'''{ cls.name }/{ name }'''
            if bp_name in PLUGINS: raise Exception(f'''{ bp_name } - Already Registered!''')
            clean_form = { k:None for k in fields }
            PLUGINS[ bp_name ] = lambda: function(clean_form)
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                results = function(*args, **kwargs)
                return results
            return wrapper
        return real_decorator


#dyClass = lambda name: type(name, (), {})
