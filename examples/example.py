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
print( data )
data = vuenicfy.vuetify.records()
print( data )
data = vuenicfy.vuetify.update()
print( data )
data = vuenicfy.vuetify.delete()
print( data )

@vuenicfy.vuetify.decorator("arg1", "arg2")
def print_args(*args): pass
print_args(1,2)

bp = vuenicfy.vuetify.Blueprint('user')

@bp.route
def bad_moffo(name): print('bad moffo')

#bad_moffo('hello')
print( bp.blueprints.bad_moffo() )
