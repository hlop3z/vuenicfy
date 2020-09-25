from . import register_plugin
import re
from collections import namedtuple

RESPONSE			= namedtuple('Schema', ['error', 'data', 'method'])
_isRegex			= lambda d: False if d is None else True
isRegex				= lambda t,s: _isRegex(  re.search(t, str( s ))  )


def replace(text, items):
    for selector, replacement in items: text=re.sub(selector, replacement, text)
    return text

@register_plugin
def easy_regex(letters='a-zA-Z0-9', min_size=0):
    return "^([" + letters + "]{" + str( min_size ) + ",})+$"

@register_plugin
def Field(value=None , **kwargs):
    fixed    = False
    auto     = False
    required = True
    rules    = []
    regex    = []
    filters  = []
    choices  = []
    method   = None

    if 'default'  in kwargs : value    = kwargs['default']
    if 'required' in kwargs : required = kwargs['required']
    if 'fixed'    in kwargs : fixed    = kwargs['fixed']
    if 'rules'    in kwargs : rules    = kwargs['rules']
    if 'filters'  in kwargs : filters  = kwargs['filters']
    if 'regex'    in kwargs : regex    = kwargs['regex']
    if 'choices'  in kwargs : choices  = kwargs['choices']
    if 'method'   in kwargs : method   = kwargs['method']

    if callable( value ):
        auto     = True
        required = False

    _form = { "default": value, "auto": auto, "required": required, "fixed": fixed,
             "rules": rules, "filters": filters, "regex": regex, "choices": choices,
             "method": method
            }
    return _form


def get_field_info(fields):
    model_keys       = set()

    auto_fields      = set()
    required_fields  = set()
    fixed_fields     = set()

    filters_fields   = set()
    regex_fields     = set()

    rules_fields     = set()
    choices_fields   = set()
    method_fields    = set()

    for name, schema in fields.items():
        if not schema: schema = Field()
        model_keys.add( name )
        if 'auto'     in schema and schema['auto']    : auto_fields.add    ( name )
        if 'required' in schema and schema['required']: required_fields.add( name )
        if 'fixed'    in schema and schema['fixed']   : fixed_fields.add   ( name )
        if 'rules'    in schema and schema['rules']   : rules_fields.add   ( name )
        if 'choices'  in schema and schema['choices'] : choices_fields.add ( name )
        if 'method'   in schema and schema['method']  : method_fields.add  ( name )
        if 'filters'  in schema and schema['filters'] : filters_fields.add ( name )
        if 'regex'    in schema and schema['regex']   : regex_fields.add   ( name )

    bp = namedtuple('Fields', ["keys", "auto", "required", "fixed", "rules", "choices", "method", "filters", "regex"])
    return bp(model_keys, auto_fields, required_fields, fixed_fields, rules_fields, choices_fields, method_fields, filters_fields, regex_fields)






class Schema:
    def __init__(self, __name__ = None, **kwargs):
        self.schema = kwargs
        self.info   = get_field_info( kwargs )

    def setup(self, form):
        fields       = self.schema
        info         = self.info

        # Required Fields
        error_data   = [ k for k in info.required if k not in form ]
        if error_data:  return RESPONSE(True, error_data, 'required')

        # Choice Fields
        for k in [ k for k in info.choices if k in form ]:
            if not isinstance(form[ k ], list): val = [ form[ k ] ]
            else                              : val = form[ k ]
            found_error = [x for x in val if x not in fields[ k ]['choices'] ]
            if found_error: error_data.append( k )
        if error_data:  return RESPONSE(True, error_data, 'choices')

        # Rule Fields
        for k in [ x for x in info.rules if x in form ]:
            valid = all([ r( form[ k ] ) for r in fields[ k ]['rules'] ])
            if not valid: error_data.append( k )
        if error_data:  return RESPONSE(True, error_data, 'rules')

        # Filters Fields
        for k in [ x for x in info.filters if x in form ]:
            form[ k ] = replace( form[ k ], fields[ k ]['filters'] )

        # Regex Fields
        for k in [ x for x in info.regex if x in form ]:
            isvalid = all([  isRegex( r, form[ k ] ) for r in fields[ k ]['regex']  ])
            if not isvalid: error_data.append( k )
        if error_data:  return RESPONSE(True, error_data, 'regex')

        # Automated Fields
        for k in info.auto: form[ k ] = fields[ k ]['default']()

        # Method Fields
        for k in info.method:
             if k in form: form[ k ] = fields[ k ]['method']( form[ k ] )

        return RESPONSE(False, form, 'form')


    def update(self, form):
        response = self.setup( form )
        schema   = response.data
        if not response.error:
            for k in self.info.fixed:
                del schema[ k ]
            return RESPONSE(False, schema, 'update')
        return response

    def create(self, form):
        response = self.setup( form )
        schema   = { k:None for k in self.info.keys }
        if not response.error:
            schema.update( response.data )
            for k,v in schema.items():
                if not v: schema[ k ] = self.schema[ k ]['default']
            return RESPONSE(False, schema, 'create')
        return response
