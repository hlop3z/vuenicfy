async def custom_handler( handler, payload ):
    m1 = await handler.read_row(**{ "model": "users", "fields": ['*'], "query": {"id":{ "eq":1 }} })
    print( "Custom Function - el TOXIC" )
    print( payload )
    if m1['error']: return m1
    else:
        """Do Something else with the data"""
        m2 = await handler.read(**{ "model": "users", "fields": ['*'], "query": None })
        return m2
