# MODULES
from . import schemas
from . import __demo__
from . import vuetify



# STRUCTURE
__plugins__ = {
"schemas" : schemas.__dir__(),
"__demo__" : __demo__.__dir__(),
"vuetify" : vuetify.__dir__(),
}