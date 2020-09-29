import sys

sys.path.append('../vuenicfy')

import vuenicfy

SQLiteSanic = vuenicfy.sqlitemin.SQLiteSanic

# Schema < INIT >
from users import Users
from wallets import Wallets

Schemas = [ Users, Wallets ]
ltsanic = SQLiteSanic( Schemas )

# Models < register >
users   = ltsanic.model['users']
wallets = ltsanic.model['wallets']

from handler import custom_handler as users_handler

# Model-Handler < register >
users.route( users_handler )

ltsanic.app.run(host='0.0.0.0', port=8055)
