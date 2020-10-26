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



def order_by(sort=None):
    if sort is None           : OUTPUT=f"{ offset_text }"
    elif sort.startswith('-') : OUTPUT=f"ORDER BY { sort.replace('-', '', 1) } DESC"
    else                      : OUTPUT=f"ORDER BY { sort } ASC"
    return OUTPUT



def pagination(page=None, size=None):
    offset = (page - 1) * size
    if offset>0: offset_text = f"LIMIT { size } OFFSET { offset }"
    else       : offset_text = f"LIMIT { size }"
    return offset_text



class Sqlow:
    def __init__(self, table=None, pk="id", sqlite=False):
        self.table  = table
        self.pk     = pk
        self.sqlite = sqlite

    def find(self, query={}, fields=['*'], sort_by=None, page=None):
        _query, args = make_sql_where(query = query, sqlite = self.sqlite)
        queryText = f'SELECT { ",".join( fields ) } FROM { self.table } { _query if _query else "" }'
        if sort_by: queryText += f" { order_by( sort_by ) }"
        if page   : queryText += f" { pagination( **page ) }"
        if not self.sqlite: return ( f"{ queryText };", *args )
        return                     ( f"{ queryText };", (*args,) )

    def create(self, form={}):
        pgkeys = lambda: ",".join( [f"${ i+1 }" for i,k in enumerate(form.keys())] )
        ltkeys = lambda: ",".join( ["?" for k in form.keys()] )
        queryText = lambda ks: f'''INSERT INTO { self.table }({ ",".join( form.keys() ) }) VALUES ({ ks })'''
        if not self.sqlite: return (f"{ queryText( pgkeys() ) } RETURNING *;", *form.values())
        return (f"{ queryText( ltkeys() ) };", (*form.values(),))

    def update(self, form=None, query=None):
        _query, args = make_sql_update(form = form, query = query, sqlite = self.sqlite)
        queryText = f'UPDATE { self.table } { _query };'
        if not self.sqlite: return ( queryText, *args )
        return                     ( queryText, (*args,) )

    def delete(self, query=None):
        _query, args = make_sql_where(query = query, sqlite = self.sqlite)
        queryText = f'DELETE FROM { self.table } { _query };'
        if not self.sqlite: return ( queryText, *args )
        return                     ( queryText, (*args,) )
