# Intro

**This is a work in progress**

This provides a very simple way of deploying a Django project to production. There are other solutions for using CherryPy, but this further simplifies things by serving static and media files automatically provided you have the usual Django MEDIA\_\* and STATIC\_\* settings and generally setting sensible defaults for small sites.

The motivation for creating this was the realisation of just how many Django sites were running on small VPSes, but using solutions that were suited to high traffic sites running on servers with large numbers of cores.

# Settings

The following settings are all optional:

* EASYSERVER_IP - the IP address to bind. Defaults to 0.0.0.0  (all available IPs)
* EASYSERVER_PORT - port to bind. Defaults to 80. You will need to change this or configure the system for appropriate privileges on unix like OSes.
* CHEROOT - a dict of any keyword params accepted by Cheroot's [cheroot.wsgi.Server](https://cheroot.cherrypy.dev/en/latest/pkg/cheroot.wsgi/). Defaults to {} but this is NOT the same as cheroot for all defaults.


# TODO

These are the major features still missing:

* https support
* Acme support to get TLS certificates for https
* Simplifying usage of ports 80 and 443
* Logging
* Tests

Dealing with ports is OS specific and is likely to be supported only on Linux. It is fairly simple to fix manually so is a low priority.


# Use cases

1. Low traffic sites.
2. API servers, and other cases where static content is absent or very limited (e.g. only an admin panel).
3. Where assets are served from a CDN.
4. Sites running on small VPSes

The server is threaded Python so is probably not suitable where performance is an issue and CPU bound within the python because of the GIL. C libraries (such as DB clients) will often work threaded.

## Advantages

* Simplicity of deployment - no need to configure a separate web server
* Django locmem cache *should* work well

## Disadvantages

* Will not scale well for some/many use cases
* Not as well tested as more popular solutions
* Static file serving will almost certainly be relatively inefficient
