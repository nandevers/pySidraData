# Contributing to pySidraData

Small, focused improvements are welcome: clearer examples, reproducible bug reports, metadata handling and API error handling.

## Report an issue

Include your Python and dependency versions, the aggregate ID or public IBGE endpoint involved, a minimal example, the error message, and expected versus observed behavior. Remove credentials and non-public data.

## Propose a change

Describe the problem and the intended behavior before submitting a substantial change. Keep pull requests focused and explain compatibility effects. The repository's existing tests are located in `pySidraData/tests`; describe any checks you performed without claiming checks you did not run.

Installation metadata is in `pyproject.toml` and `setup.py`; development dependencies are listed in `requirements-dev.txt`. Python-version compatibility and the installation path should be checked in the intended environment.

## Documentation

Keep examples tied to actual public API methods. Label illustrative output and avoid unsupported CI or coverage badges. Existing examples are under `examples/`.
