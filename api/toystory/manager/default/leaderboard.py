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

from oslo.config import cfg
conf = cfg.CONF

from toystory.manager import base
from toystory.utils import async


class DefaultLeaderboardController(base.LeaderboardController):

    def get(self, sort, period):
        # TODO(TheSriram): works based on commits and period is entire history
        # changeup according to function signature soon.
        access_token = conf.github.access_token
        urls = [conf.github.stats_url.format(repo) + '?access_token={0}'.format(conf.github.access_token) for repo in conf.github.repos]
        responses = async.async_request('GET',urls)
        return {repo: response for (repo, response) in zip(conf.github.repos,responses)}




