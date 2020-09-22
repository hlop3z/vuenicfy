from . import register_plugin

@register_plugin
class Plugin:
    def hello(self):
        print("Hello from < Class >")


@register_plugin
def hello():
    print("Hello from < Function >")
