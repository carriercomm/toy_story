Toy Story
============

Getting Started
---------------

#. From your /toy_story/api folder::

#. Install general requirements::

    $ pip install -r requirements/requirements.txt

#. Start the web server::

    $ gunicorn toystory:app

#. Test everything is working by requesting the root URL::

    $ curl -i -H http://0.0.0.0:8888/

   You should get an **HTTP 200** along with some headers that will look similar to this::

    HTTP/1.0 200 OK
    Date: Tue, 15 Jul 2014 12:44:16 GMT
    Server: WSGIServer/0.1 Python/2.7.6
    Content-Length: 16
    Content-Type: application/json; charset=UTF-8

    {"status": "up"}
