import functools

from . import register_plugin
from .crud_handler import CrudHandler

@register_plugin
class Handler:
    def __init__(self, pool=None, models=None, payload={}, blueprints=None):
        self.pool       = pool
        self.models     = models
        self.payload    = payload
        self.blueprints = blueprints

    def database(self, f):
        pool        = self.pool
        models      = self.models
        payload     = self.payload
        blueprints  = self.blueprints
        @functools.wraps(f)
        async def decorated_function(*args, **kwargs):
            async with pool.acquire() as connection:
                async with connection.transaction():
                    try                  : return {'error': False,
                                                   'data': await f(CrudHandler(connection, models, payload, blueprints), *args, **kwargs),
                                                   'method': 'postgres'
                                            }
                    except Exception as e: return {'error': True, 'data': e.args, 'method': 'postgres'}
        return decorated_function

    @staticmethod
    def crud_info():
        text = {
        "list": '''
payload = {
    "url"  : "<model>/list",
    "data" : {
        "fields": ['*'],
        "query" : [
            { "id": { "gt" : 100000 } },
            "or",
            {"id": { "in" : [1,2,3,4] }},
        ]
    }
}
        '''.strip(),

        "find": '''
payload = {
    "url"  : "<model>/find",
    "data" : {
        "fields": ['*'],
        "query" : { "id": { "eq" : 1 } }
    },
}
        '''.strip(),

        "create": '''
payload = {
    "url"  : "<model>/create",
    "data" : { "id": 1 }
}
        '''.strip(),

        "update": '''
payload = {
    "url"  : "<model>/update",
    "data" : {
        "form"  : { "name": f'user-test' },
        "query" : { "id": { "eq" : 1 } }
    }
}
        '''.strip(),

        "delete": '''
payload = {
    "url"  : "<model>/delete",
    "data" : { "id": { "eq" : 1 } }
}
        '''.strip(),
        }
        return text
