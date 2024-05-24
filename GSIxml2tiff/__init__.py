def classFactory(iface):
    from .MyPlugin import MyPlugin
    return MyPlugin(iface)
