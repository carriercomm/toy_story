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

import uuid

from toystory.storage import base


class MemoryTodosController(base.TodosController):

    def __init__(self, driver):
        super(MemoryTodosController, self).__init__(driver)

        # {'project_id': [{'id': 'uuid', 'title': 'Title', 'text': 'Text'}]}
        self._data = {}

    def list(self, project_id):
        if project_id in self._data:
            return self._data[project_id]

        return []

    def get(self, project_id, todo_id):
        if project_id not in self._data:
            return None

        todos = self._data[project_id]

        return next((todo for todo in todos if todo['id'] == todo_id), None)

    def create(self, project_id, title, text):
        if project_id not in self._data:
            self._data[project_id] = []

        todo = {'id': uuid.uuid4(), 'title': title, 'text': text}
        self._data[project_id].append(todo)

        return todo

    def update(self, project_id, todo_id, title, text):
        todo = self.get(project_id, todo_id)

        if todo is None:
            # TODO(bryansd): Raise error
            return None

        todo['title'] = title
        todo['text'] = text

        return todo

    def delete(self, project_id, todo_id):
        if project_id not in self._data:
            return True

        todo = self.get(project_id, todo_id)
        if todo is not None:
            self._data[project_id].remove(todo)

        return True
