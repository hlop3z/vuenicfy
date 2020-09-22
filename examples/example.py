import sys

sys.path.append('../vuenicfy')

import vuenicfy

# Modules
print( vuenicfy.__plugins__ )

# Class
vuenicfy.__demo__.Plugin().hello()

# Def
#vuenicfy.__demo__.hello()
vuenicfy.vuetify.hello()
