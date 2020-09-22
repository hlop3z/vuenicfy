import sys

sys.path.append('../vuenicfy')

import vuenicfy

# Modules
#print( vuenicfy.__plugins__ )

# Class
#vuenicfy.__demo__.Plugin().hello()

# Def
#vuenicfy.__demo__.hello()
data = vuenicfy.vuetify.create()
data = vuenicfy.vuetify.records()
print( data )
data = vuenicfy.vuetify.update()
data = vuenicfy.vuetify.delete()

@vuenicfy.vuetify.decorator("arg1", "arg2")
def print_args(*args): pass

bp = vuenicfy.vuetify.Blueprint('user')

@bp.route(fields=['name', 'idz'])
def bad_moffo(form, update):
    print( form )
    return update

#print( bp.urls )
d = bp.plugins['user/bad_moffo']({ "name":'ablaze', "id":'ablaze' })
print( d )
