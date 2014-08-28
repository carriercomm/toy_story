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

"""Default manager driver implementation."""

from toystory.common import decorators
from toystory.manager import base
from toystory.manager.default import controllers


class DefaultManagerDriver(base.Driver):

    def __init__(self, conf, storage):
        super(DefaultManagerDriver, self).__init__(conf, storage)

    @decorators.lazy_property(write=False)
    def leaderboard_controller(self):
        """Returns the driver's Leaderboard controller."""
        return controllers.Leaderboard(self)

    @decorators.lazy_property(write=False)
    def badges_controller(self):
        """Returns the driver's Badge controller."""
        return controllers.Badges(self)
