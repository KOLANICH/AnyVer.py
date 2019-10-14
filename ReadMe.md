AnyVer.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
=========
![GitLab Build Status](https://gitlab.com/KOLANICH/AnyVer.py/badges/master/pipeline.svg)
[wheel (GHA via `nightly.link`)](https://nightly.link/prebuilder/AnyVer.py/workflows/CI/master/AnyVer-0.CI-py3-none-any.whl)
![GitLab Coverage](https://gitlab.com/prebuilder/AnyVer.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/prebuilder/AnyVer.py.svg)](https://coveralls.io/r/prebuilder/AnyVer.py)
[![GitHub Actions](https://github.com/prebuilder/AnyVer.py/workflows/CI/badge.svg)](https://github.com/prebuilder/AnyVer.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/prebuilder/AnyVer.py.svg)](https://libraries.io/github/prebuilder/AnyVer.py)

Just a version parsing library.

Extracts numbers, their formats and a hex-number (available as `hash`) from version strings. Allows comparisons (`>`, `<` and `==`) and editing. Allows accessing components separately using numeric indices. Allows iteration. First 4 components are available as properties `major`, `minor`, `patch` and `tweak`.

See [`tests/tests.py`](./tests/tests.py) for the examples.

Requirements
------------
* [`Python 3`](https://www.python.org/downloads/).
