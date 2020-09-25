import sys

sys.path.append('../vuenicfy')

import vuenicfy

field      = vuenicfy.schemas.Field
easy_regex = vuenicfy.schemas.easy_regex

import hashlib, time

def hash_password(value):
    return hashlib.blake2s( value.encode('utf-8'), digest_size=8 ).hexdigest()

_isPass     = lambda v: """^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\\\?\/\|!@#\$%\^&\*><,\."'])(?=.{"""+str(v)+""",})"""
isPass      = _isPass(8) # AT LEAST ONE OF EACH (a-z, A-Z, 0-9) and AT LEAST ONE OF ( . , \ / < > ? ! @ # $ % ^ & * | )
isUsername  = easy_regex('a-z0-9_', 2)
isPhone     = '^\+?(\d.*){6,}$'

schema = {
    "id"        : field( required=False  ),
    "group"     : field( None, choices=['customers', 'admins', 'employees', 'partners', 'investors'] ),
    "username"  : field( regex=[ isUsername ], validators=[ (lambda v: "__" not in v) ]  ),
    "password"  : field( method=hash_password,  regex=[ isPass ]  ),
    "phone"     : field( regex=[ isPhone ], rules=[ (lambda v: "--" not in v) ], required=False  ),
    "modified"  : field( lambda: int( time.time() ) ),
    "timestamp" : field( lambda: int( time.time() ), fixed=True ),
}

#bp = vuenicfy.schemas.Blueprint('user', schema = schema, sqlite = True)

#@bp.route
def bad_moffo():
    print( "Hello" )
    return None

print( bp.urls )
d = bp.method['user/create']({ 'group':'admins' ,'username':'admin', 'password':'#Secre1password' })
print( d )
