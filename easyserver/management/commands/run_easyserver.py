from pathlib import Path

from cheroot.wsgi import Gateway_10  # WSGI 1.0 subclass
from cheroot.server import HTTPServer

from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application

from django.conf import settings


def get_well_known_root():
    """Create a root directory for .well-known if not specified"""
    well_known = Path(settings.BASE_DIR) / 'well_known_root'
    well_known.mkdir(exist_ok=True)
    return well_known


# Get relevant settings

easyserver_settings = {
    **{
        'SERVE_STATIC': True,
        'IP': '0.0.0.0',
        'PORT': 80,
    },
    **getattr(settings, 'EASYSERVER', {}),
}

if 'WELL_KOWN_ROOT' not in easyserver_settings:
    easyserver_settings['WELL_KOWN_ROOT'] = get_well_known_root()

print(easyserver_settings)

# cheroot settings have some overrides of original cheroot defaults
cheroot_defaults = {
    #  TODO replace based on number of CPUs
    'minthreads': 3,  # a good default for a small VPS
    'gateway': Gateway_10
}


class Server(HTTPServer):
    """Subclass specific to this command"""

    def __init__(self, addr, wsgi_app, **kwargs):
        super().__init__(
            addr,
            **{**cheroot_defaults, **kwargs}
        )
        self.wsgi_app = wsgi_app
        self.max_request_body_size = kwargs.get(
            'max_request_body_size',
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE + settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        )


def get_static_app(root):
    """Return a WSGI app that serves static files from root"""
    root_obj = Path(root)

    def serve_static(fpath, start_response):
        # FIXME - this is insecure and requires path check to prevent ../ etc
        full_path = root_obj / fpath
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
        except (IsADirectoryError, FileNotFoundError):
            start_response('404 Not Found', [])
            return [b'<h1>Not found</h1>']
        # TODO need to return content types
        start_response('200 OK', [])
        return [content]
    return serve_static


def get_dispatcher():
    serve_static = easyserver_settings['SERVE_STATIC']
    if not serve_static:
        return get_wsgi_application()
    # paths can only be top level dir
    # replace assertions with checks. Ensure directory exists
    static_path = settings.STATIC_URL.strip('/').split('/')
    assert len(static_path) == 1
    media_path = settings.MEDIA_URL.strip('/').split('/')
    assert len(media_path) == 1
    path_map = {
        static_path[0]: get_static_app(settings.STATIC_ROOT),
        # TODO deal correctly with MEDIA_ROOT not set.
        media_path[0]: get_static_app(settings.MEDIA_ROOT),
    }
    paths = {static_path[0], media_path[0]}
    if easyserver_settings['WELL_KOWN_ROOT']:
        paths.add('.well_known')
        path_map['.well_known/'] = get_static_app(easyserver_settings['WELL_KOWN_ROOT'])
    app = get_wsgi_application()

    def dispatch(environ, start_response):
        split_path = [p for p in environ['PATH_INFO'].split('/') if p]
        if not (split_path and (split_path[0] in paths)):
            return app(environ, start_response)
        assert len(split_path) >= 2
        return path_map[split_path[0]]('/'.join(split_path[1:]), start_response)
    return dispatch


class Command(BaseCommand):
    help = 'Run a production quality server'

    def handle(self, *args, **options):
        server = Server(
            (easyserver_settings['IP'], easyserver_settings['PORT']),
            get_dispatcher()
        )
        print('starting:', server)
        server.start()
