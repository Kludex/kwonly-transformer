<h1 align="center">
    <strong>kwonly-transformer</strong>
</h1>
<p align="center">
    <a href="https://pypi.org/project/kwonly-transformer" target="_blank">
        <img src="https://img.shields.io/pypi/v/kwonly-transformer" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/kwonly-transformer">
    <img src="https://img.shields.io/github/license/Kludex/kwonly-transformer">
</p>

This is a very opinionated tool. The idea is that we want functions with multiple parameters to have **exclusively** keyword only parameters.

As an example, let's consider a function with multiple parameters. When we are reading the call for that function,
we lose time either checking the reference, or trying to map in our brains what argument matches a specific function parameter.
```python
def do_something(a, b, c, d, e, f):
    ...

do_something(True, "potato", 1, "haha", None, False)
```
`kwonly-transformer` is a tool that formats the above into the following:

```python
def do_something(*, a, b, c, d, e, f):
    ...

do_something(a=True, b="potato", c=1, d="haha", e=None, f=False)
```

## Installation

```bash
pip install kwonly-transformer
```

## License

This project is licensed under the terms of the MIT license.
