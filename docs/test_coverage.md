# Test Coverage

Test coverage shows how much of the code is exercised by automated tests.

## How to check test coverage locally

Install `coverage` if not already installed:

```bash
pip install coverage
```
Run tests with coverage enabled:
```bash
coverage run -m pytest tests/
```
Generate a coverage report:
```bash
coverage report
```
---
## Example Output
```matlib
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/__init__.py                      0      0   100%
src/cohere_api.py                   8      1    88%
src/commands.py                   123     64    48%
src/config.py                      12      0   100%
src/tmdb_api.py                    64     54    16%
src/vote_database.py               16     10    38%
tests/test_cohere_api.py           12      0   100%
tests/test_tmdb_api.py             47      0   100%
-----------------------------------------------------
TOTAL                             282    129    54%

```