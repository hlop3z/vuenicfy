from sanic import Sanic
from sanic import response
import asyncpg

import sys

sys.path.append('../vuenicfy')

import vuenicfy
Users = vuenicfy.schemas.Blueprint('users', schema = { "name" : None, "dob" : None }, sqlite = False)

app = Sanic()

@app.listener('before_server_start')
async def setup_pool(app, loop):
    app.postgres = await asyncpg.create_pool(user='username', password='password', database='mewb', host='127.0.0.1', port=5432)

from functools import wraps
#fetchval, fetchrow, fetch, execute
def database(f):
    @wraps(f)
    async def decorated_function(request, *args, **kwargs):
        pool = request.app.postgres
        async with pool.acquire() as connection:
            async with connection.transaction():
                try:
                    results = await f(request, connection, *args, **kwargs)
                    return response.json( {'error': False, 'data': results, 'method': f.__name__} )
                except Exception as e:
                    return response.json( {'error': True, 'data': e, 'method': 'database'} )
    return decorated_function

@app.route('/')
@database
async def test(request, tx):
    values = [dict(r) for r in await tx.fetch('SELECT * FROM users;')]
    return values

@app.route('/info')
async def test(request):
    return response.json( {'error': False, 'data': Users.form.info._asdict(), 'method': Users.name } )

@app.post('/post')
@database
async def test(request, tx):
    payload = request.json['data']
    url     = request.json['url']
    q = Users.method[ url ]( payload )
    values = await tx.fetchval( *q.data )
    if not q.error: return values
    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8055)
