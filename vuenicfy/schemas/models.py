from collections import namedtuple

PLUGINS  = dict()
RESPONSE = namedtuple('Schemas', ['error', 'data', 'method'])

class Models:
    def __init__(self, name=None, schema=None, pk=None, sqlite=False):
        self.name      = name
        self.form      = Schema( **schema )
        self.sql       = Sqlow( name, pk = pk, sqlite = sqlite )

        def create( form=None ):
            create = self.form.create( form )
            if not create.error: return RESPONSE(False, self.sql.create( create.data ), 'sql-create')
            return create

        def update( form=None, query=None ):
            update = self.form.update( form )
            if not update.error: return RESPONSE(False, self.sql.update( update.data, query ), 'sql-update')
            return update

        def find( query={}, fields=['*'], sort_by=None, page=None ):
            return RESPONSE(False, self.sql.find( query, fields, sort_by, page ), 'sql-where')

        def delete( query=None ):
            return RESPONSE(False, self.sql.delete( query ), 'sql-delete')

        self.route( create )
        self.route( update )
        self.route( delete )
        self.route( find )



    def route(cls, function):
        # Set-Name
        bp_name = f'''{ cls.name.lower() }'''
        name    = function.__name__
        # Set-SchemaBase
        if not bp_name in PLUGINS: PLUGINS[ bp_name ] = { "info": cls.form.meta._asdict() }
        # Register Function
        if name in PLUGINS[ bp_name ]: raise Exception(f'''Function: < { name } > inside Schema: < { bp_name } > is Already Registered!''')
        else                         : PLUGINS[ bp_name ][ name ] = function
