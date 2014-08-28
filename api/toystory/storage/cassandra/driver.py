# Copyright (c) 2014 Rackspace, Inc.
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

"""Cassandra storage driver implementation."""

from cassandra import cluster
from cassandra import query

from toystory.common import decorators
from toystory.storage import base
from toystory.storage.cassandra import controllers

from oslo.config import cfg

CASSANDRA_OPTIONS = [
    cfg.ListOpt('cluster', help='Cassandra Cluster contact points'),
    cfg.StrOpt('keyspace', default='toystory',
               help='Keyspace for all queries made in session'),
]

CASSANDRA_GROUP = 'drivers:storage:cassandra'


def _connection(conf):
    cassandra_cluster = cluster.Cluster(conf.cluster)
    session = cassandra_cluster.connect(conf.keyspace)
    session.row_factory = query.dict_factory

    return session


class CassandraStorageDriver(base.Driver):

    def __init__(self, conf):
        super(CassandraStorageDriver, self).__init__(conf)

        self._conf.register_opts(CASSANDRA_OPTIONS,
                                 group=CASSANDRA_GROUP)
        self.cassandra_conf = self._conf[CASSANDRA_GROUP]

    def is_alive(self):
        return True

    @decorators.lazy_property(write=False)
    def connection(self):
        """Cassandra connection instance."""
        return _connection(self.cassandra_conf)

    @decorators.lazy_property(write=False)
    def repos_controller(self):
        return controllers.ReposController(self)

    @decorators.lazy_property(write=False)
    def _database(self):
        return self.connection
