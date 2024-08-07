# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud import datastore
import pytest

import query_multi_ineq as snippets

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def entities():
    client = datastore.Client(project=PROJECT_ID)

    tasks = [
        {"description": "Buy milk", "priority": 0, "days": 10},
        {"description": "Feed cats", "priority": 10, "days": 10},
        {"description": "Play with dog", "priority": 10, "days": 1},
    ]

    employees = [
        {"name": "Alice", "salary": 100_000, "experience": 10},
        {"name": "Bob", "salary": 80_000, "experience": 2},
        {"name": "Charlie", "salary": 120_000, "experience": 10},
        {"name": "David", "salary": 90_000, "experience": 3},
        {"name": "Eve", "salary": 110_000, "experience": 9},
        {"name": "Joe", "salary": 110_000, "experience": 7},
        {"name": "Mallory", "salary": 200_000, "experience": 0},
    ]

    for task in tasks:
        task_key = client.key("Task")
        task_entity = datastore.Entity(key=task_key)
        task_entity.update(task)
        client.put(task_entity)
    for employee in employees:
        employee_key = client.key("employees")
        employee_entity = datastore.Entity(key=employee_key)
        employee_entity.update(employee)
        client.put(employee_entity)


    yield entities

    client.delete(task1)
    client.delete(task2)


def test_query_filter_compound_multi_ineq(entities):
    query = snippets.query_indexing_considerations()
    results = list(query.stream())
    assert len(results) == 1
    assert results[0].to_dict()["description"] == "Play with dog"


def test_query_indexing_considerations(entities):
    query = snippets.query_indexing_considerations()
    results = list(query.stream())
    # should contain employees salary > 100_000 sorted by salary and experience
    assert len(results) == 3
    assert results[0].to_dict()["name"] == "Charlie"
    assert results[1].to_dict()["name"] == "Eve"
    assert results[2].to_dict()["name"] == "Joe"


def test_query_order_fields(entities):
    results = snippets.query_indexing_considerations()
    assert len(results) == 4
    assert results[0].to_dict()["name"] == "Mallory"
    assert results[1].to_dict()["name"] == "Joe"
    assert results[2].to_dict()["name"] == "Eve"
    assert results[3].to_dict()["name"] == "Charlie"
