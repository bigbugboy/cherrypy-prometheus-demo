import cherrypy
from prometheus_client import start_http_server

from midleware import PrometheusMiddleware


class App:
    @cherrypy.expose
    def index(self):
        return 'index'

    @cherrypy.expose
    def about(self):
        return 'about'


cherrypy.config.update({
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 9898,
})


cherrypy_app = cherrypy.tree.mount(App(), '/', None)


# register prometheus middleware for cherrypy app
cherrypy_app.wsgiapp.pipeline.append(('PrometheusMiddleware', PrometheusMiddleware))

# run a http server for prometheus server fetch metrics data
start_http_server(8999)


cherrypy.engine.start()
cherrypy.engine.block()
