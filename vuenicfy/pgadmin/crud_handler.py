class CrudHandler:
    '''CrudHandler:
create      (**{ "model": "name", "form": {} })
read_row    (**{ "model": "name", "fields": ['*'], "query": {} })
read        (**{ "model": "name", "fields": ['*'], "query": {} })
update      (**{ "model": "name", "form": {}, "query": {} })
delete      (**{ "model": "name", "query": {} })
    '''
    def __init__(self, tx=None, models=None, payload={}, blueprints=None):
        self.tx         = tx
        self.models     = models
        self.payload    = payload
        self.blueprints = blueprints

    async def create(self, model=None, form={}):
        tx     = self.tx
        models = self.models
        active = models[ model ][ 'create' ]( form )
        if not active.error:
            data = { "form":form, "id": await tx.fetchval( *active.data ) }
            return { 'error': active.error, 'data': data                            , 'method': active.method }
        else:
            return { 'error': active.error, 'data': active.data                     , 'method': active.method }


    async def read_row(self, model=None, fields=['*'], query=None):
        tx     = self.tx
        models = self.models
        active = models[ model ][ 'read' ]( fields=fields, query=query )
        if not active.error:
            _data  = await tx.fetchrow( *active.data )
            if _data: data = dict( _data )
            else    : data = {}
            return { 'error': active.error, 'data': data                            , 'method': active.method }
        else:
            return { 'error': active.error, 'data': active.data                     , 'method': active.method }


    async def read(self, model=None, fields=['*'], query=None):
        tx     = self.tx
        models = self.models
        active = models[ model ][ 'read' ]( fields=fields, query=query )
        if not active.error:
            _data  = await tx.fetch( *active.data )
            if _data: data = [ dict( r ) for r in _data ]
            else    : data = []
            return { 'error': active.error, 'data': data                            , 'method': active.method }
        else:
            return { 'error': active.error, 'data': active.data                     , 'method': active.method }


    async def update(self, model=None, form={}, query=None):
        tx     = self.tx
        models = self.models
        active = models[ model ][ 'update' ]( form=form, query=query )
        if not active.error:
            await tx.execute( *active.data )
            return { 'error': active.error, 'data': {"form": form, "query": query}  , 'method': active.method }
        else:
            return { 'error': active.error, 'data': active.data                     , 'method': active.method }


    async def delete(self, model=None, query=None):
        tx     = self.tx
        models = self.models
        active = models[ model ][ 'delete' ]( query )
        if not active.error:
            await tx.execute( *active.data )
            return { 'error': active.error, 'data': query                           , 'method': active.method }
        else:
            return { 'error': active.error, 'data': active.data                     , 'method': active.method }


    async def handler( self ):
        handler     = self
        blueprints  = handler.blueprints
        url         = handler.payload['url']
        payload     = handler.payload['data']
        parts       = list(filter( lambda x: x.strip() != '', url.split('/') ))
        custom      = False
        if len( parts ) == 3:
            custom = True
            model  = parts[0]
            method = parts[2]
        else:
            model  = parts[0]
            method = parts[1]
        if not custom:
            if   method == "create": m1 = await handler.create(**{ "model": model, "form" : payload })
            elif method == "delete": m1 = await handler.delete(**{ "model": model, "query": payload })
            elif method == "update": m1 = await handler.update(**{ "model": model, "form": payload['form'], "query": payload['query'] })
            elif method == "list"  : m1 = await handler.read(**{ "model": model, "fields": payload['fields'], "query": payload['query'] })
            elif method == "find"  : m1 = await handler.read_row(**{ "model": model, "fields": payload['fields'], "query": payload['query'] })
        else:
            m1 = await blueprints[f"{ model }/{ method }"](handler, payload)
        return m1
