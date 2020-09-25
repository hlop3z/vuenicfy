import os
from string import Template


def postgres_account( username = "username", password = "password" ):
    os.system( f"""unset HISTFILE""" )
    os.system( f"""sudo -u postgres createuser -s -i -d -r -l -w  { username }""" )
    s = "'"
    os.system( f'''sudo -u postgres psql -c "ALTER ROLE { username } WITH PASSWORD {s}{ password }{s}"''')


def create_database( database="ablaze_testing" ):
    os.system( f"""sudo -u postgres psql -c 'CREATE DATABASE { database };'""" )


def delete_database( database="ablaze_testing" ):
    os.system( f"""sudo -u postgres psql -c 'DROP DATABASE { database };'""" )

#postgres_account()
