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

from pecan import hooks

from toystory.openstack.common import context
from toystory.openstack.common import local


class ContextHook(hooks.PecanHook):

    def on_route(self, state):
        context_kwargs = {}

        request_context = context.RequestContext(**context_kwargs)
        state.request.context = request_context
        local.store.context = request_context

    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        state.response.headers[
            'Access-Control-Allow-Headers'] = 'origin, authorization, accept'
        if not state.response.headers['Content-Length']:
            state.response.headers[
                'Content-Length'] = str(len(state.response.body))
