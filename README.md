# flake8-empty-init-modules

flake8 plugin that disallows code in `__init__.py` modules.

## installation

```sh
python -m pip install flake8-empty-init-modules
```

## checks

### EIM001

Disallows all code in any `__init__.py` module.

### EIM002

Allows imports and assignment to `__all__` in `__init__.py` modules, but nothing
else.

This check is disabled by default. To use this check instead of `EIM001` add the
following to your `setup.cfg`

```ini
[flake8]
ignore = EIM001
enable-extensions=EIM002
```

## rationale

Code in `__init__.py` modules is often unwanted because:

- it runs at import-time - this can cause surprising import-time side-effects
- these modules are often empty, so code there is easily missed

The relaxed version of this check allows convenience imports in `__init__.py`
modules without allowing 'real' code to hide out there.
