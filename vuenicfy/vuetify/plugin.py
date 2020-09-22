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


class Skeleton: pass

@register_plugin
class Blueprint:
    def __init__(self, name=None):
        self.blueprints = type(name, (), {})

    def route(cls, function):
        """ decorator without arguments """
        name = function.__name__
        setattr(cls.blueprints, name, function)
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            results = function(*args, **kwargs)
            return results
        return wrapper



#dyClass = lambda name: type(name, (), {})
