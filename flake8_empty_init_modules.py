from __future__ import annotations

import ast
import os.path
from typing import Any
from typing import Iterable
from typing import Iterator


class EIM001:
    message = 'EIM001 code in `__init__.py` module'

    def __init__(self, tree: ast.AST, filename: str, lines: Iterable[str]):
        self.filename = filename
        self.lines = lines

    def run(self) -> Iterator[tuple[int, int, str, type[Any]]]:
        if os.path.basename(self.filename) != '__init__.py':
            return

        yield from (
            (lineno, 0, self.message, type(self))
            for lineno, line in enumerate(self.lines, start=1)
            if line.strip()
        )


class _EIM002Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[int] = []

    def _is_import(self, node: ast.AST) -> bool:
        return isinstance(node, (ast.Import, ast.ImportFrom))

    def _is_dunder_all_assignment(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Assign)
            and all(
                target.id == '__all__'  # type: ignore[attr-defined]
                for target in node.targets
            )
        )

    def _is_docstring(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )

    def _is_for_convenience_imports(self, node: ast.AST) -> bool:
        return any((
            self._is_import(node),
            self._is_dunder_all_assignment(node),
            self._is_docstring(node),
        ))

    def visit_Module(self, node: ast.Module) -> Any:
        self.errors += [
            node_.lineno
            for node_ in node.body
            if not self._is_for_convenience_imports(node_)
        ]

        super().generic_visit(node)


class EIM002:
    off_by_default = True

    message = 'EIM002 non-import code in `__init__.py` module'

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.filename = filename
        self.tree = tree

    def run(self) -> Iterator[tuple[int, int, str, type[Any]]]:
        if os.path.basename(self.filename) != '__init__.py':
            return

        visitor = _EIM002Visitor()
        visitor.visit(self.tree)

        for lineno in visitor.errors:
            yield lineno, 0, self.message, type(self)
