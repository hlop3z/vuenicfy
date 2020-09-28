import sys

sys.path.append('../vuenicfy')

import vuenicfy

Field   = vuenicfy.schemas.Field
PgSanic = vuenicfy.pgadmin.PgSanic

Schemas = [
    {
        "name": "users",
        "schema": {
            "name" : None,
            "dob"  : Field( rules=[ (lambda v: "x" not in str(v)) ], required=False  ),
        }
    },
    {
        "name": "wallets",
        "schema": {
            "name" : None,
            "dob"  : Field( rules=[ (lambda v: "x" not in str(v)) ], required=False  ),
        }
    },
]

pg      = PgSanic( Schemas )
users   = pg.model['users']
wallets = pg.model['wallets']

@users.route
async def custom_handler( handler, payload ):
    m1 = await handler.read_row(**{ "model": "users", "fields": ['*'], "query": {"id":{ "eq":1 }} })
    print( "Custom Function - el TOXIC" )
    if m1['error']: return m1
    else:
        """Do Something else with the data"""
        m2 = await handler.read(**{ "model": "users", "fields": ['*'], "query": None })
        return m2


pg.app.run(host='0.0.0.0', port=8055)
