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

@bp.route(fields=['name'])
def bad_moffo(form):
    form['name'] = 'ablaze'
    return form

#print( bp.urls )
d = bp.plugins['user/bad_moffo']()
print( d )
