from pathlib import Path

from cheroot.wsgi import Server, PathInfoDispatcher

from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application

from django.conf import settings


# directory as a Path object
static_root = Path(settings.STATIC_ROOT)


def get_static_app(root):
    """Return a WSGI app that serves static files from root"""
    root_obj = Path(root)

    def serve_static(environ, start_response):
        # FIXME - this is insecure and requires path check to prevent ../ etc
        print(environ['PATH_INFO'])
        full_path = root_obj / environ['PATH_INFO'].lstrip('/')
        # TODO deal with directories and 404
        with open(full_path, 'rb') as f:
            content = f.read()
        # TODO need to return content types
        start_response('200 OK', [])
        return [content]
    return serve_static


class Command(BaseCommand):
    help = 'Run a production quality server'

    def handle(self, *args, **options):
        server = Server(
            ('127.0.0.1', 8080),
            PathInfoDispatcher(
                {
                    '/' + settings.STATIC_URL.lstrip('/'):
                        get_static_app(settings.STATIC_ROOT),
                    '/' + settings.MEDIA_URL.lstrip('/'):
                        get_static_app(settings.MEDIA_ROOT),
                    '/': get_wsgi_application()
                }
            )
        )
        server.start()
