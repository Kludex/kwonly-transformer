import sys
import textwrap

import libcst as cst
import pytest

from kwonly_transformer import CallArgumentsTransformer, FunctionParametersTransformer


@pytest.mark.parametrize(
    "input,expected_func,expected_call_args",
    (
        pytest.param(
            textwrap.dedent(
                """
            def home(a, b, c, *, d=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(*, a, b, c, d=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(a, b, c, *, d=None):
                ...

            home(a=1, b=2, c=3)
            """
            ),
            id="function",
        ),
        pytest.param(
            textwrap.dedent(
                """
            async def home(a, b, c, *, d=None):
                ...

            await home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            async def home(*, a, b, c, d=None):
                ...

            await home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            async def home(a, b, c, *, d=None):
                ...

            await home(a=1, b=2, c=3)
            """
            ),
            id="async",
        ),
        pytest.param(
            textwrap.dedent(
                """
            def home(a, b, *, d=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(a, b, *, d=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(a, b, *, d=None):
                ...

            home(1, 2, c=3)
            """
            ),
            id="below threshold",
        ),
        pytest.param(
            textwrap.dedent(
                """
            def home(a, /, b, c, d=None, *, e=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(a, /, *, b, c, d=None, e=None):
                ...

            home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            def home(a, /, b, c, d=None, *, e=None):
                ...

            home(1, b=2, c=3)
            """
            ),
            id="posonly params",
            marks=pytest.mark.skipif(
                sys.version_info < (3, 8),
                reason="Python 3.7 doesn't support posonly arguments.",
            ),
        ),
        pytest.param(
            textwrap.dedent(
                """
            class Potato:
                def home(a, b, c, *, d=None):
                    ...

            Potato().home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            class Potato:
                def home(*, a, b, c, d=None):
                    ...

            Potato().home(1, 2, c=3)
            """
            ),
            textwrap.dedent(
                """
            class Potato:
                def home(a, b, c, *, d=None):
                    ...

            Potato().home(a=1, b=2, c=3)
            """
            ),
            id="objects",
        ),
    ),
)
def test_transformer(input: str, expected_func: str, expected_call_args: str) -> None:
    source_tree = cst.parse_module(input)
    function_transformer = FunctionParametersTransformer()
    modified_tree = source_tree.visit(function_transformer)
    assert modified_tree.code == expected_func
    call_args_transformer = CallArgumentsTransformer(function_transformer.functions)
    modified_tree = source_tree.visit(call_args_transformer)
    assert modified_tree.code == expected_call_args
