SQL_OPS = {
    # EQUAL
    "eq"   : lambda column, value    : (f'''{ column } = { value }'''),
    # NOT EQUAL
    "!eq"  : lambda column, value    : (f'''{ column } != { value }'''),

    # BETWEEN
    "bt"   : lambda column, low, high: (f'''{ column } > { low } AND { column } < { high }'''),
    # NOT BETWEEN
    "!bt"  : lambda column, low, high: (f'''{ column } < { low } OR  { column } > { high }'''),

    # BETWEEN include LOW & HIGH
    "be"   : lambda column, low, high: (f'''{ column } >= { low } AND { column } <= { high }'''),
    # NOT BETWEEN include LOW & HIGH
    "!be"  : lambda column, low, high: (f'''{ column } <= { low } OR  { column } >= { high }'''),

    # IN
    "in"   : lambda column, array    : (f'''{ column } IN ({ ",".join( array ) })'''),
    # NOT IN
    "!in"  : lambda column, array    : (f'''{ column } NOT IN ({ ",".join( array ) })'''),

    # MATCH STRING PATTERN
    "like" : lambda column, pattern  : (f'''{ column } LIKE { pattern }'''),
    # NOT MATCH STRING PATTERN
    "!like": lambda column, pattern  : (f'''{ column } NOT LIKE { pattern }'''),

    # GREATER THAN
    "gt"   : lambda column, value    : (f'''{ column } > { value }'''),
    # GREATER OR EQUAL THAN
    "ge"   : lambda column, value    : (f'''{ column } >= { value }'''),
    # LESS THAN
    "lt"   : lambda column, value    : (f'''{ column } < { value }'''),
    # LESS OR EQUAL THAN
    "le"   : lambda column, value    : (f'''{ column } <= { value }''')
}



def make_sql_where(query=[], index=0, sqlite=False):
    sql_text = []
    values   = []
    if not query  : return None, []
    if isinstance(query, dict): query = [ query ]
    for q in query:
        if isinstance(q, str):
            sql_text.append( q.upper() )
        else:
            key, args = list(q.items())[0]
            args      = list(args.items())[0]
            method    = args[0]
            value     = args[1]
            _count    = 0

            if   method in ["bt", "!bt", "be", "!be"]: _count = 2
            elif method in ["in", "!in"]             : _count = len( value )
            else                                     : _count = 1
            if sqlite: _index = [ '?' for i in range( _count ) ]
            else     : _index = [ f'${ (index + (i + 1)) }' for i in range( _count ) ]
            index += _count

            if   method in ["bt", "!bt", "be", "!be"]: OUT = SQL_OPS[ method ](key, _index[0], _index[1])
            elif method in ["in", "!in"]             : OUT = SQL_OPS[ method ](key, _index)
            else                                     : OUT = SQL_OPS[ method ](key, _index[0])
            sql_text.append( OUT )
            if isinstance(value, list): values += value
            else                      : values.append( value )
    return f'WHERE { " ".join(sql_text) }', values



def _make_sql_update(form=None, sqlite=False):
    index    = 0
    sql_text = []
    values   = []
    for k,v in form.items():
        index += 1
        if sqlite: _index = f"{ k }=?"
        else     : _index = f"{ k }=${ index }"
        sql_text.append( _index )
        values.append( v )
    return (f'''SET { ", ".join( sql_text ) }''', values, len( form.keys() ))



def make_sql_update(form=None, query=None, sqlite=False):
    sql_update, update_values, index = _make_sql_update( form, sqlite = sqlite )
    sql_query, query_values = make_sql_where( query = query, sqlite = sqlite, index = index )

    out_sql  = (f"{ sql_update } { sql_query }")
    out_vals = (update_values + query_values)
    return out_sql, out_vals



class Sqlow:
    def __init__(self, table=None, sqlite=False):
        self.table  = table
        self.sqlite = sqlite

    def find(self, query={}, fields=['*']):
        _query, args = make_sql_where(query = query, sqlite = self.sqlite)
        if not self.sqlite: return (f'SELECT { ",".join( fields ) } FROM { self.table } { _query if _query else "" };', *args)
        return                     (f'SELECT { ",".join( fields ) } FROM { self.table } { _query if _query else "" };', (*args,))

    def create(self, form={}):
        if not self.sqlite: return (f'''INSERT INTO { self.table }({ ",".join( form.keys() ) }) VALUES ({ ",".join( [f"${ i+1 }" for i,k in enumerate(form.keys())] ) }) RETURNING id;''', *form.values())
        else              : _fields = ",".join( ["?" for k in form.keys()] )
        return (f'''INSERT INTO { self.table }({ ",".join( form.keys() ) }) VALUES ({ ",".join( ["?" for k in form.keys()] ) });''', (*form.values(),))

    def update(self, form=None, query=None):
        _query, args = make_sql_update(form = form, query = query, sqlite = self.sqlite)
        if not self.sqlite: return (f'UPDATE { self.table } { _query };', *args)
        return                     (f'UPDATE { self.table } { _query };', (*args,))

    def delete(self, query=None):
        _query, args = make_sql_where(query = query, sqlite = self.sqlite)
        if not self.sqlite: return (f'DELETE FROM { self.table } { _query };', *args)
        return                     (f'DELETE FROM { self.table } { _query };', (*args,))
