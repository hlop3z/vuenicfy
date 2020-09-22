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
