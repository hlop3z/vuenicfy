# MODULES
from . import pgadmin
from . import schemas
from . import sqlitemin
from . import __demo__
from . import vuetify



# STRUCTURE
__plugins__ = {
"pgadmin" : pgadmin.__dir__(),
"schemas" : schemas.__dir__(),
"sqlitemin" : sqlitemin.__dir__(),
"__demo__" : __demo__.__dir__(),
"vuetify" : vuetify.__dir__(),
}