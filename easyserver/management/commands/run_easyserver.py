from pathlib import Path

from cheroot.wsgi import Server, PathInfoDispatcher

from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application

from django.conf import settings


# directory as a Path object
static_root = Path(settings.STATIC_ROOT)


def serve_static(environ, start_response):
    """A simple WSGI application to return a static file"""
    # FIXME - this is insecure and requires path check to prevent ../ etc
    full_path = static_root / environ['PATH_INFO'].lstrip('/')
    # TODO deal with directories and 404
    with open(full_path, 'rb') as f:
        content = f.read()
    # TODO need to return content types
    start_response('200 OK', [])
    return [content]


class Command(BaseCommand):
    help = 'Run a production quality server'

    def handle(self, *args, **options):
        server = Server(
            ('127.0.0.1', 8080),
            PathInfoDispatcher(
                {
                    '/' + settings.STATIC_URL.lstrip('/'): serve_static,
                    '/': get_wsgi_application()
                }
            )
        )
        server.start()
