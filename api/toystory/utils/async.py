import functools

import asyncio
import aiohttp
import json


from toystory.utils.event_loop import get_event_loop


def _noloop_request(method, url):
    first_response = yield from aiohttp.request(method=method, url=url)
    second_response = yield from first_response.content.read()
    current_response = [dict(user = response['author']['login'],
                             commits = response['total'],
                             gravatar = response['author']['avatar_url'])
                        for response in json.loads(second_response.decode())]

    sorted_resp = sorted(current_response, key=lambda k: k['commits'], reverse=True)

    return sorted_resp
    # return second_response.decode()


@get_event_loop
def async_request(method, urls):

    tasks = [asyncio.Task(_noloop_request(method='GET',url=url)) for url in urls]
    total_responses = yield from asyncio.gather(*tasks)

    return total_responses





