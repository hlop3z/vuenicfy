import collections, asyncpg

from sanic import Sanic
from sanic import response

from ..schemas import Blueprints
from .handler import Handler
from . import register_plugin
from .sqlitemin import Sqlitemin

@register_plugin
def SQLiteSanic( schemas ):
    BPS         = Blueprints(schemas, sqlite = True)
    Sqlow       = BPS.schemas
    CUSTOMBPS   = BPS.custom

    app = Sanic()

    async def sqlite_handler( handler ):
        return await handler.handler()

    sqlite_pool  = Sqlitemin()

    @app.listener('before_server_start')
    async def setup_postgres(app, loop):
        create_table = """CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        name text,
        dob INTEGER
        )"""
        #await sqlite_pool.execute( create_table )
        async def sqlite_tx(payload={}, pool=sqlite_pool):
            method      = sqlite_handler
            handler     = Handler(pool, Sqlow.methods, payload, CUSTOMBPS)
            data        = await handler.database( method )()
            output      = {'error': True, 'data': None, 'method': 'handler' }
            if not data['error']: output.update( data['data'] )
            else                : output.update( data )
            return response.json( output )

        app.sqlite  = sqlite_tx


    @app.post('/post')
    async def database_sqlite(request):
        sqliteDB = request.app.sqlite
        return await sqliteDB( request.json )


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

    RESPONSE = collections.namedtuple('Sqlite_Sanic', ['app', 'model'])
    return RESPONSE(app, BPS.find)
