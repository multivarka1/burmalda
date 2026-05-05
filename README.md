# burmalda

`burmalda` is a tiny Python library that prints `Burmalda` to the console when
your program exits because of an unhandled exception.

## Installation

```bash
pip install burmalda
```

## Usage

Install the exception hook near the start of your program:

```python
import burmalda

burmalda.install()

raise RuntimeError("Something broke")
```

The program will still show the normal Python traceback, and `Burmalda` will be
printed to standard error before it.

## API

### `burmalda.install(message="Burmalda")`

Installs the global exception hook and returns the previous `sys.excepthook`.
Calling it more than once is safe.

### `burmalda.uninstall()`

Restores the exception hook that was active before `burmalda.install()`.

### `burmalda.burmalda(message="Burmalda")`

A context manager that installs the hook temporarily:

```python
import burmalda

with burmalda.burmalda():
    raise RuntimeError("Something broke")
```

