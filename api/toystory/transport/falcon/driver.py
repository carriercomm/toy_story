# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
from wsgiref import simple_server

import falcon
from oslo.config import cfg
import six

from toystory import transport
from toystory.openstack.common import log
from toystory.transport.falcon import leaderboard


_WSGI_OPTIONS = [
    cfg.StrOpt('bind', default='127.0.0.1',
               help='Address on which the self-hosting server will listen'),

    cfg.IntOpt('port', default=8888,
               help='Port on which the self-hosting server will listen'),

    cfg.IntOpt('content_max_length', default=256 * 1024),
    cfg.IntOpt('metadata_max_length', default=64 * 1024)
]

_WSGI_GROUP = 'drivers:transport:falcon'

LOG = log.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class DriverBase(transport.DriverBase):

    def __init__(self, conf, manager):
        super(DriverBase, self).__init__(conf, manager)

        self._conf.register_opts(_WSGI_OPTIONS, group=_WSGI_GROUP)
        self._wsgi_conf = self._conf[_WSGI_GROUP]

        self._manager = manager

        self.app = None
        self._init_routes()

    def after_hooks(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers', 'origin, authorization, accept')

    def _init_routes(self):
        """Initialize hooks and URI routes to resources."""
        self.app = falcon.API(after=[self.after_hooks])

        self.app.add_route(
            '/v1.0/{org}/{repo}/leaderboard', leaderboard.ItemResource(self._manager.leaderboard_controller))

    def listen(self):
        """Self-host using 'bind' and 'port' from the WSGI config group."""

        msgtmpl = (u'Serving on host %(bind)s:%(port)s')
        LOG.info(msgtmpl,
                 {'bind': self._wsgi_conf.bind, 'port': self._wsgi_conf.port})

        httpd = simple_server.make_server(self._wsgi_conf.bind,
                                          self._wsgi_conf.port,
                                          self.app)
        httpd.serve_forever()
