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

from toystory.manager import base
from toystory.openstack.common import local


class DefaultTodosController(base.TodosController):

    def list(self):
        todos_controller = self._driver.storage.todos_controller

        return todos_controller.list(local.store.context.tenant)

    def get(self, todo_id):
        todos_controller = self._driver.storage.todos_controller

        return todos_controller.get(local.store.context.tenant, todo_id)

    def create(self, title, text):
        todos_controller = self._driver.storage.todos_controller

        return todos_controller.create(local.store.context.tenant, title, text)

    def update(self, todo_id, title, text):
        todos_controller = self._driver.storage.todos_controller

        return todos_controller.update(
            local.store.context.tenant,
            todo_id,
            title,
            text
        )

    def delete(self, todo_id):
        todos_controller = self._driver.storage.todos_controller

        return todos_controller.delete(local.store.context.tenant, todo_id)
