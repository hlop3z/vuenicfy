from . import register_plugin, frontend, backend

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
