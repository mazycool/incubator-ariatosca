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

"""
Workflow and operation decorators
"""

from uuid import uuid4
from functools import partial, wraps

from . import context
from .workflows.api import task_graph
from .tools.validation import validate_function_arguments


def workflow(
        func=None,
        simple_workflow=True,
        suffix_template=''):
    """
    Workflow decorator
    """
    if func is None:
        return partial(
            workflow,
            simple_workflow=simple_workflow,
            suffix_template=suffix_template)

    @wraps(func)
    def _wrapper(ctx, **workflow_parameters):

        workflow_name = _generate_workflow_name(
            func_name=func.__name__,
            suffix_template=suffix_template,
            ctx=ctx,
            **workflow_parameters)

        workflow_parameters.setdefault('ctx', ctx)
        workflow_parameters.setdefault('graph', task_graph.TaskGraph(workflow_name))
        validate_function_arguments(func, workflow_parameters)
        with context.workflow.current.push(ctx):
            func(**workflow_parameters)
        return workflow_parameters['graph']
    return _wrapper


def operation(
        func=None):
    """
    Operation decorator
    """
    if func is None:
        return partial(operation)

    @wraps(func)
    def _wrapper(ctx, **custom_kwargs):
        func_kwargs = _create_func_kwargs(
            custom_kwargs,
            ctx)
        validate_function_arguments(func, func_kwargs)
        ctx.description = func.__doc__
        return func(**func_kwargs)
    return _wrapper


def _generate_workflow_name(func_name, ctx, suffix_template, **custom_kwargs):
    return '{func_name}.{suffix}'.format(
        func_name=func_name,
        suffix=suffix_template.format(ctx=ctx, **custom_kwargs) or str(uuid4()))


def _create_func_kwargs(
        kwargs,
        ctx,
        workflow_name=None):
    kwargs.setdefault('graph', ctx.task_graph(workflow_name))
    return kwargs
