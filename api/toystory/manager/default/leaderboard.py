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

import asyncio
import aiohttp
import json
import datetime


from toystory.utils.event_loop import get_event_loop


class DefaultLeaderboardController(base.LeaderboardController):

    def _noloop_commits_request(self, sort, period, method, url):

        first_response = yield from aiohttp.request(method=method, url=url)

        second_response = yield from first_response.content.read()
        current_response = [dict(user=response['author']['login'],
                                 commits=sum(
                                     commits['c'] for commits in response['weeks'][period:]),
                                 gravatar=response['author']['avatar_url'])
                            for response in json.loads(second_response.decode())]

        sorted_resp = sorted(
            current_response, key=lambda k: k['commits'], reverse=True)

        return sorted_resp

    def _noloop_comments_request(self, sort, period, method, url):

        first_response = yield from aiohttp.request(method=method, url=url)

        second_response = yield from first_response.content.read()
        current_response = [dict(user=response['user']['login'],
                                 comments=(
                                     comments['body'] for comments in response),
                                 gravatar=response['user']['avatar_url'])
                            for response in json.loads(second_response.decode())]

        sorted_resp = sorted(
            current_response, key=lambda k: k['comments'], reverse=True)

        return sorted_resp


    @get_event_loop
    def async_request(self, sort, period, method, urls):

        total_responses = []

        if (sort == 'commits'):
            tasks = [asyncio.Task(
                self._noloop_commits_request(sort, period, method='GET', url=url)) for url in urls]

        elif (sort == 'comments'):
            tasks = [asyncio.Task(
                self._noloop_comments_request(sort, period, method='GET', url=url)) for url in urls]
            
        total_responses = yield from asyncio.gather(*tasks)
        return total_responses

    def get(self, sort, git_org, git_repo, weeks):
        # TODO(TheSriram): works based on commits and period is entire history
        # changeup according to function signature soon.
        if (sort == 'commits'):
            stats = "https://api.github.com/repos/{0}/{1}/stats/contributors".format(
                git_org, git_repo)
            url = stats + '?access_token={0}'.format(conf.github.access_token)

        elif (sort == 'comments'):
            since = (datetime.datetime.now() + datetime.timedelta(weeks=weeks)).isoformat()
            stats = "https://api.github.com/repos/{0}/{1}/issues/comments?since={2}".format(
                git_org, git_repo, since)

            print(stats)
            url = stats + '?access_token={0}'.format(conf.github.access_token)

        responses = self.async_request(sort, weeks, 'GET', [url])
        return responses
