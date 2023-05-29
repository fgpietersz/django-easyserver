# Intro

**This is a work in progress**

This provides a very simple way of deploying a Django project to production. There are other solutions for using CherryPy, but this further simplifies things by serving static and media files automatically provided you have the usual Django MEDIA\_\* and STATIC\_\* settings and generally setting sensible defaults for small sites.

The original idea for this came from using existing CherryPy server for Django snippets for low traffic sites and seeing ways to improve it. The motivation for creating a more elaborate solution came from the realisation the approach was also well suited to API backends even on larger sites.

# Settings

All settings are optional:

* EASYSERVER which is a dict of the following:
    * IP - the IP address to bind. Defaults to 0.0.0.0  (all available IPs)
    * PORT - port to bind. Defaults to 80. You will need to change this or configure the system for appropriate privileges on unix like OSes.
    * SERVE_STATIC - whether to serve static and media files. Defaults to True.
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
* Django locmem cache should work well
* Performance should be good for most use cases
* Lightweight and should be efficient/low resource usage

## Disadvantages

* Will not scale well for some/many use cases
* Not as well tested as more popular solutions
* Static file serving and upload will almost certainly be relatively inefficient
* CPU bound code will be limited by the Python GIL

Obviously all these will vary with your use case. If it works well then it has the advantage of simplicity. If you are concerned about performance relative to alternatives, then the only way to know either way is to test.


## Performance considerations

Performance is likely to be the main objection to the use of Django Easyserver. While it does not follow the conventional wisdom (that multi-process is preferable to threading) with regard to Python performance and scaling, there are good arguments in its favour.

The server used is Cheroot, the server from the (threaded) CherryPy framework. In most, if not all, publicly published benchmarks, CherryPy performs well. It is possible that threaded Django on Cheroot will perform worse than CherryPy on Cheroot, but there is no known reason to expect that.

On a single (virtual) core VPS threading should perform better. It cannot have worse parallelism and it has slightly lower overhead.

On a large multi-core server multiple processes should perform better.

At what point this happens will be application and configuration dependent. For example, many C libraries release the Python GIL and are thread safe so if these dominate CPU time multiple threads will make good use of multiple cores. On the other hand if you are doing a lot of heavy processing in pure Python and have sufficiently high traffic that you need this to be well parallelised (unless you have thousands of requests per hour you probably do not) then you need multiple processes.

Commonly used thread safe libraries include RDBMS clients. Performance is likely to be improved by setting a sensible value for CONN_MAX_AGE.

Because threads share memory, local memory caching should work well. This includes Django's built in locmem cache. Deployment just uses one extra setting.
