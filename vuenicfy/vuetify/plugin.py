from . import register_plugin, frontend, backend


@register_plugin
class Plugin:
    def hello(self):
        print("Hello from < Class >")


@register_plugin
def hello():
    component = frontend.Model('components')
    component.create_table('''
        name text primary key,
        data text,
        metadata text
    ''')
    component.create(name='testing')
    component.update(__query__={ "name": "testing" }, data='hello')
    component.update(__query__={ "name": "testing" }, data=None)
    component.delete( name='toxic' )
    print( component.records() )
    print("Hello from < Function >")
