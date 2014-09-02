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

import datetime
import itertools
import requests

from oslo.config import cfg
conf = cfg.CONF

from toystory.manager import base


class DefaultLeaderboardController(base.LeaderboardController):

    def get_commits(self, org, repo, weeks):
        git_url = "https://api.github.com"
        stats = git_url + "/repos/{0}/{1}/stats/contributors"
        stats = stats.format(org, repo)
        url = stats + '?access_token={0}'.format(conf.github.access_token)

        commit_stats = requests.get(url).json()

        commits = [dict(user=response['author']['login'],
                        score=sum(commits['c']
                                    for commits in response['weeks'][weeks:]),
                        gravatar=response['author']['avatar_url'])
                   for response in commit_stats]

        sorted_resp = sorted(
            commits, key=lambda k: k['score'], reverse=True)

        return sorted_resp

    def get_comments(self, org, repo, weeks):
        since = (datetime.datetime.now() + datetime.timedelta(weeks=weeks))
        since = since.isoformat()

        git_url = "https://api.github.com"
        stats = git_url + "/repos/{0}/{1}/issues/comments?since={2}"
        stats = stats.format(org, repo, since)

        url = stats + '?access_token={0}'.format(conf.github.access_token)
        comment_stats = requests.get(url).json()

        comments = [dict(user=response['user']['login'],
                         comments=1,
                         gravatar=response['user']['avatar_url'])
                    for response in comment_stats]

        key_func = lambda k: k['user']
        sorted_resp = sorted(comments, key=key_func)

        grouped_comments = []
        for key, rows in itertools.groupby(sorted_resp, key_func):
            grouped_comments.append(dict(user=key,
                                         score=sum(r['comments']
                                                      for r in rows),
                                         gravatar=''
                                         )
                                    )

        print (grouped_comments)

        sorted_comments = sorted(grouped_comments,
                                 key=lambda k: k['score'], reverse=True)

        return sorted_comments
