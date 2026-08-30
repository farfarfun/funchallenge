# NOTE: This test is intentionally minimal.
#
# funchallenge's top-level __init__.py is empty, so `import funchallenge`
# is safe. Its submodules are NOT exercised here on purpose:
#   - funchallenge.server.core executes real code at *module import time*
#     (it instantiates DbBase(), which reads a secret and opens a real
#     database connection, and then runs a live SQL query), so importing
#     it would perform network/database I/O as a side effect of running
#     the test suite.
#   - funchallenge.db.base depends on funsecret's `read_secret`, which is
#     only safe to *call* (inside DbBase.__init__), not necessarily to
#     import, in a credential-less offline environment.
# This repo also has no dependency-management block to add a `pytest`
# dev dependency to (it uses a plain setup.py built on the internal
# `funpypi.setup` wrapper), so setup.py is left untouched.
import funchallenge


def test_import_funchallenge():
    assert funchallenge is not None
