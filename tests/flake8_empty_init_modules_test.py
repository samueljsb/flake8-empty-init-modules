from __future__ import annotations

import ast

from flake8_empty_init_modules import EIM001
from flake8_empty_init_modules import EIM002

PYTHON_MODULE = '''\
"""This is the module docstring."""

# convenience imports:
import os
from pathlib import Path

__all__ = ['MY_CONSTANT']

MY_CONSTANT = 5
"""This is an important constant."""

os.environ['FOO'] = 1
'''


class TestEIM001:
    def _run(self, file_name, module):
        return set(
            EIM001(
                tree=ast.parse(module),
                filename=file_name,
                lines=module.splitlines(keepends=True),
            ).run(),
        )

    def test_empty_init_module(self):
        assert self._run('my_package/__init__.py', '') == set()

    def test_init_module_with_code(self):
        assert self._run('my_package/__init__.py', PYTHON_MODULE) == {
            (1, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (3, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (4, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (5, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (7, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (9, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (10, 0, 'EIM001 code in `__init__.py` module', EIM001),
            (12, 0, 'EIM001 code in `__init__.py` module', EIM001),
        }

    def test_non_init_module(self):
        assert self._run('my_package/some_module.py', PYTHON_MODULE) == set()


class TestEIM002:
    def _run(self, file_name, module):
        return set(EIM002(tree=ast.parse(module), filename=file_name).run())

    def test_empty_init_module(self):
        assert self._run('my_package/__init__.py', '') == set()

    def test_init_module_with_code(self):
        assert self._run('my_package/__init__.py', PYTHON_MODULE) == {
            (9, 0, 'EIM002 non-import code in `__init__.py` module', EIM002),
            (12, 0, 'EIM002 non-import code in `__init__.py` module', EIM002),
        }

    def test_non_init_module(self):
        assert self._run('my_package/some_module.py', PYTHON_MODULE) == set()
