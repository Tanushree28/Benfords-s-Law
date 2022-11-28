from wsgiref.simple_server import make_server
from pyramid.config import Configurator

if __name__ == "__main__":
    # Configuring the web app
    with Configurator() as config:
        # External package included in the app
        config.include('pyramid_jinja2')
        # config.include('pyramid_debugtoolbar')

        # Adding static file path
        config.add_static_view(name="static", path="static")

        # Urls/Routes
        config.add_route('home', '/')
        config.add_route('result', '/result-of-distribution/{filename}')
        config.add_route('error', '/error/{error_type}')

        # Accessing the views methods
        config.scan('views')

        app = config.make_wsgi_app()
    
    # Creating and Configurating the server    
    server = make_server('0.0.0.0', 6545, app)
    server.serve_forever()