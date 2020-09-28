from sanic import Sanic
from sanic import response
import asyncpg

import functools
import sys

sys.path.append('../vuenicfy')

import vuenicfy

Handler     = vuenicfy.pgadmin.Handler
Field       = vuenicfy.schemas.Field

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

bps         = vuenicfy.schemas.Blueprints(Schemas, sqlite = False)
Sqlow       = bps.schemas
CUSTOMBPS   = bps.custom

users       = bps.find['users']
wallets     = bps.find['wallets']

app = Sanic()


@users.route
async def custom_handler( handler, payload ):
    m1 = await handler.read_row(**{ "model": "users", "fields": ['*'], "query": {"id":{ "eq":1 }} })
    print( "Custom Function" )
    if m1['error']: return m1
    else:
        """Do Something else with the data"""
        m2 = await handler.read(**{ "model": "users", "fields": ['*'], "query": None })
        return m2


async def postgres_handler( handler ):
    return await handler.handler()

@app.listener('before_server_start')
async def setup_postgres(app, loop):
    postgres_pool = await asyncpg.create_pool(user='username', password='password', database='mewb', host='127.0.0.1', port=5432)

    async def postgres_tx(payload={}, pool=postgres_pool):
        method      = postgres_handler
        handler     = Handler(pool, Sqlow.methods, payload, CUSTOMBPS)
        data        = await handler.database( method )()
        output      = {'error': True, 'data': None, 'method': 'handler' }
        if not data['error']: output.update( data['data'] )
        else                : output.update( data )
        return response.json( output )

    app.postgres  = postgres_tx


@app.post('/post')
async def database_postgres(request):
    postgresDB = request.app.postgres
    return await postgresDB( request.json )


@app.route('/')
async def app_info(request):
    urls = set()
    for k in Sqlow.keys:
        urls.add(f'{ k }/create')
        urls.add(f'{ k }/update')
        urls.add(f'{ k }/find')
        urls.add(f'{ k }/list')
        urls.add(f'{ k }/delete')
    return response.json( {'error': False, 'data': {
        'schemas'   : Sqlow.info,
        'urls'      : sorted(list( urls )),
        "crud"      : Handler.crud_info(),
        'custom'    : CUSTOMBPS.keys()
        }, 'method': f"app-info" } )


@app.route('/info/<name:[A-z]+>')
async def schema_info(request, name):
    info = Sqlow.methods[ name ]['info']
    return response.json( {'error': False, 'data': info, 'method': f"info-{ name }" } )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8055)
