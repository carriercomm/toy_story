
import asyncio
import aiohttp
import json


from toystory.utils.event_loop import get_event_loop


def _noloop_request(sort, period,method, url):

    first_response = yield from aiohttp.request(method=method, url=url)

    second_response = yield from first_response.content.read()
    current_response = [dict(user = response['author']['login'],
                             commits = sum(commits['c'] for commits in response['weeks'][period:]),
                             gravatar = response['author']['avatar_url'])
                        for response in json.loads(second_response.decode())]

    sorted_resp = sorted(current_response, key=lambda k: k['commits'], reverse=True)

    return sorted_resp


@get_event_loop
def async_request(sort,period,method, urls):

    tasks = [asyncio.Task(_noloop_request(sort, period, method='GET',url=url)) for url in urls]
    total_responses = yield from asyncio.gather(*tasks)

    return total_responses





