import sys

sys.path.append('../vuenicfy')

import vuenicfy

Field   = vuenicfy.schemas.Field

Users = {
    "name": "users",
    "schema": {
        "name" : None,
        "dob"  : Field(
            rules       = [ (lambda v: "x" not in str(v)) ],
            required    = False
        ),
    }
}

import peewee
from playhouse.postgres_ext import PostgresqlExtDatabase

def SqliteModel( DATABASE ):
    database = peewee.SqliteDatabase( DATABASE )
    class BaseModel( peewee.Model ):
        class Meta:
            database = database
    return BaseModel

def PgModel( database='my_app', user='postgres', password='secret', host='10.1.0.9', port=5432 ):
    extdatabase = peewee.PostgresqlExtDatabase(database, user=user, password=password, host=host, port=port)
    class BaseModel( peewee.Model ):
        class Meta:
            database = extdatabase
    return BaseModel
