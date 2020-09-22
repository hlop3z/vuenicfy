from . import register_plugin
from .engine import Sqlite

@register_plugin
class Plugin:
    def hello(self):
        print("Hello from < Class >")


@register_plugin
def hello():
    print("Hello from < Function >")
