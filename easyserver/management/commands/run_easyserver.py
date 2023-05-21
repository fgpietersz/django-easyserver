from cheroot.wsgi import Server

from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application


class Command(BaseCommand):
    help = 'Run a production quality server'

    def handle(self, *args, **options):
        server = Server(
            ('127.0.0.1', 8080),
            get_wsgi_application()
        )
        server.start()
