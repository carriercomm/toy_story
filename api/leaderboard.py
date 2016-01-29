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

import json
import requests
import os


class LeaderboardItem(object):

    def on_get(self, req, resp, org, repo):
        sort = req.get_param('sort')
        weeks = req.get_param_as_int('weeks')
        github_token = os.environ['GITHUB_TOKEN']
        git_url = "https://api.github.com"

        if (sort == "commits"):
            url = "{0}/repos/{1}/{2}/stats/contributors?access_token={3}".format(
                git_url, org, repo, github_token)
            commit_stats = requests.get(url).json()

            commits = [dict(user=response['author']['login'],
                            score=sum(commits['c']
                                      for commits in response['weeks'][weeks:]),
                            gravatar=response['author']['avatar_url'])
                       for response in commit_stats]

            board = sorted(
                commits, key=lambda k: k['score'], reverse=True)

            result = json.dumps(board)
            resp.body = (result)


