import sys

sys.path.append('../vuenicfy')

import vuenicfy

Field   = vuenicfy.schemas.Field

Wallets = {
    "name": "wallets",
    "schema": {
        "name" : None,
        "dob"  : Field(
            rules       = [ (lambda v: "x" not in str(v)) ],
            required    = False
        ),
    }
}
