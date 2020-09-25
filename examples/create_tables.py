import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='username', password='password', database='mewb', host='127.0.0.1', port=5432)
    values = await conn.execute("""
        CREATE TABLE users(
        id serial PRIMARY KEY,
        name text,
        dob INTEGER
    )""")
    #values = await conn.execute('''DROP TABLE users''')
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete( run() )
