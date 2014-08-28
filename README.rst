Finding Dory
============
A reference project for Python APIs based on OpenStack. In particular, this project uses:

* oslo.config
* pecan
* stevedore

Getting Started
---------------
#. From your home folder, create the ``~/.toystory`` folder and clone this repository::

    $ cd ~
    $ mkdir .toystory
    $ git clone https://github.com/rackerlabs/finding_toystory.git

#. Copy the configuration files to the directory ``~/.toystory``::

    $ cp finding_toystory/etc/toystory.conf ~/.toystory/toystory.conf
    $ cp finding_toystory/etc/logging.conf ~/.toystory/logging.conf

#. For logging, find the ``[DEFAULT]`` section in ``~/.toystory/toystory.conf`` and modify as desired::

    log_file = server.log

#. Install general requirements::

    $ pip install -r requirements/requirements.txt

#. Run the following so you can see the results of any changes you make to the code without having to reinstall the package each time::
    
    $ pip install -e .

#. Start the web server::

    $ toystory-server

#. Test everything is working by requesting the root URL with a sample project ID::

    $ curl -i -H "X-Project-Id: 123" http://0.0.0.0:8888/

   You should get an **HTTP 200** along with some headers that will look similar to this::

    HTTP/1.0 200 OK
    Date: Tue, 15 Jul 2014 12:44:16 GMT
    Server: WSGIServer/0.1 Python/2.7.6
    Content-Length: 16
    Content-Type: application/json; charset=UTF-8

    {"status": "up"}
