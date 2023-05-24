# Intro

**This is a work in progress**

This provides a very simple way of deploying a Django project to production. Therea re other solutions for using CherryPy, but this further simplifies things by serving static and media files automatically provided you have the usual Django MEDIA\_\* and STATIC\_\* settings.

It is suitable for certain use cases:

1. Low traffic sites.
2. API servers, and other cases where static content is absent or very limited (e.g. only an admin panel).
3. Where assets are served from a CDN.

The server is threaded Python so is probably not suitable where performance is an issue and CPU bound within the python because of the GIL. C libraries (such as DB clients) will often work threaded.

# Settings

The following settings are all optional:

EASYSERVER_IP - the ip address to bind. Defaults to 0.0.0.0  (all available IPs)
EASYSERVER_PORT - port to bind. Defaults to 80. You will need to change this or configure the system for appropriate privileges on unix like OSes.
CHEROOT - a dict of any keyword params accepted by Cheroot's [cheroot.wsgi.Server](https://cheroot.cherrypy.dev/en/latest/pkg/cheroot.wsgi/)


# TODO

These are the major features still missing:

* https support
* Acme support to get TLS certificates for https
* Simplifying usage of ports 80 and 443
* Tests

The last of these is OS specific and is likely to be support only on Linux.
