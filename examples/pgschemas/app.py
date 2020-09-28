import sys

sys.path.append('../vuenicfy')

import vuenicfy

PgSanic = vuenicfy.pgadmin.PgSanic

# Schema < INIT >
from users import Users
from wallets import Wallets

Schemas = [ Users, Wallets ]
pgsanic = PgSanic( Schemas )

# Models < register >
users   = pgsanic.model['users']
wallets = pgsanic.model['wallets']

from handler import custom_handler as users_handler

# Model-Handler < register >
users.route( users_handler )

pgsanic.app.run(host='0.0.0.0', port=8055)
