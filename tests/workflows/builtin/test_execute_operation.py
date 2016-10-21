# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from aria.workflows.api import task
from aria.workflows.builtin.execute_operation import execute_operation

from ... import mock
from . import ctx_with_basic_graph


@pytest.fixture
def ctx():
    return ctx_with_basic_graph()


def test_execute_operation(ctx):
    operation_name = mock.operations.NODE_OPERATIONS_INSTALL[0]
    node_instance_id = 'dependency_node_instance'

    execute_tasks = list(
        task.WorkflowTask(
            execute_operation,
            ctx=ctx,
            operation=operation_name,
            operation_kwargs={},
            allow_kwargs_override=False,
            run_by_dependency_order=False,
            type_names=[],
            node_ids=[],
            node_instance_ids=[node_instance_id]
        ).topological_order()
    )

    assert len(execute_tasks) == 1
    assert execute_tasks[0].name == '{0}.{1}'.format(node_instance_id, operation_name)

# TODO: add more scenarios
