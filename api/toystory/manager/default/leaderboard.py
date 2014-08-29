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

    def get(self, sort, git_org, git_repo, weeks):
        # TODO(TheSriram): works based on commits and period is entire history
        # changeup according to function signature soon.
        stats = "https://api.github.com/repos/{0}/{1}/stats/contributors".format(
            git_org, git_repo)
        url = stats + '?access_token={0}'.format(conf.github.access_token)

        responses = async.async_request(sort, weeks, 'GET', [url])

        return responses
