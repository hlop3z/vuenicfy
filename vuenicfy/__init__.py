# MODULES
from . import __demo__
from . import vuetify



# STRUCTURE
__plugins__ = {
"__demo__" : __demo__.__dir__(),
"vuetify" : vuetify.__dir__(),
}