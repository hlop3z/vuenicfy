import collections, asyncpg

from sanic import Sanic
from sanic import response

from ..schemas import Blueprints
from .handler import Handler
from . import register_plugin

@register_plugin
def PgSanic( schemas ):
    BPS         = Blueprints(schemas, sqlite = False)
    Sqlow       = BPS.schemas
    CUSTOMBPS   = BPS.custom

    app = Sanic()

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


    @app.route('/<name:[A-z]+>')
    async def schema_info(request, name):
        info = Sqlow.methods[ name ]['info']
        return response.json( {'error': False, 'data': info, 'method': f"info-{ name }" } )

    RESPONSE = collections.namedtuple('Postgres_Sanic', ['app', 'model'])
    return RESPONSE(app, BPS.find)
