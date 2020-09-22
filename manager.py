import subprocess, argparse, json, pathlib, shutil, os

PROJECT = pathlib.Path(__file__).resolve().parents[0]
cmd     = lambda x: subprocess.run(x, check=True, shell=True)

PLUGIN_INIT = '''
from importlib import import_module
from importlib import resources

PLUGINS = dict()

def register_plugin(func):
    """Decorator to register plug-ins"""
    name = func.__name__
    PLUGINS[name] = func
    return func

def __getattr__(name):
    """Return a named plugin"""
    try:
        return PLUGINS[name]
    except KeyError:
        _import_plugins()
        if name in PLUGINS:
            return PLUGINS[name]
        else:
            raise AttributeError(
                f"module {__name__!r} has no attribute {name!r}"
            ) from None

def __dir__():
    """List available plug-ins"""
    _import_plugins()
    return list( PLUGINS.keys() )

def _import_plugins():
    """Import all resources to register plug-ins"""
    for name in resources.contents(__name__):
        if name.endswith(".py"):
            import_module(f"{__name__}.{name[:-3]}")
    '''.strip()





PLUGIN_EXAMPLE = '''
from . import register_plugin

@register_plugin
class Plugin:
    def hello(self):
        print("Hello from < Class >")


@register_plugin
def hello():
    print("Hello from < Function >")
'''.strip()



def set_modules_init():
    try:
        PROJECT_MODULES     = list(filter(lambda x: x not in ["__pycache__"], [ x for x in os.walk( f"{ PROJECT }/{ PROJECT.name }") ][0][1]))
        MODULES_IMPORT_TEXT = "\n".join([f"from . import { module }"for module in PROJECT_MODULES])
        MODULES_METHODS     = "\n".join( [ f'''"{ module }" : { module }.__dir__(),''' for module in PROJECT_MODULES] )
        _ob_                = "{"
        _cb_                = "}"
        MODULES_TEXT        = f"""
# MODULES
{ MODULES_IMPORT_TEXT }



# STRUCTURE
__plugins__ = { _ob_ }
{ MODULES_METHODS }
{ _cb_ }
        """.strip()
        with open(f"{ PROJECT.name }/__init__.py", "w") as f:
            f.write( MODULES_TEXT )
            f.close()
    except Exception as e:
        pass



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('module', nargs=1, help='''Create new "Module" for your project.''')
    args = parser.parse_args()

    if args.module:
        app_name = args.module[0].lower().replace('-','_').strip()
        app_path = f"{ PROJECT.name }/{ app_name }"

        try : os.mkdir( app_path )
        except Exception as e: pass

        with open(f"{ app_path }/__init__.py", "w") as f:
            f.write( PLUGIN_INIT )
            f.close()

        with open(f"{ app_path }/example.py", "w") as f:
            f.write( PLUGIN_EXAMPLE )
            f.close()

        set_modules_init()

    else: pass


if __name__ == '__main__':
    main()
