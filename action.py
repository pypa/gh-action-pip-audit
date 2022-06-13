#!/usr/bin/env python3

# action.py: run pip-audit
#
# most state is passed in as environment variables; the only argument
# is a whitespace-separated list of inputs

import os
import sys
import subprocess
from pathlib import Path


def _pip_audit(*args):
    return ["python", "-m", "pip_audit", *args]


def _fatal_help(msg):
    print(msg)
    subprocess.run(_pip_audit("--help"))
    sys.exit(1)


inputs = [Path(p).resolve() for p in sys.argv[1].split()]

# The arguments we pass into `pip-audit` get built up in this list.
pip_audit_args = []

if os.getenv("GHA_PIP_AUDIT_REQUIRE_HASHES", "false") != "false":
    pip_audit_args.append("--require-hashes")

if (
    service := os.getenv("GHA_PIP_AUDIT_VULNERABILITY_SERVICE", "pypi").lower()
) != "pypi":
    pip_audit_args.extend(["--service", service])

# If inputs is empty, we let `pip-audit` run in "pip source" mode by not
# adding any explicit input argument(s).
# Otherwise, we handle either exactly one project path (a directory)
# or one or more requirements-style inputs (all files).
if len(inputs) != 0:
    for input_ in inputs:
        if input_.is_dir():
            if len(inputs) != 1:
                _fatal_help("pip-audit only supports one project directory at a time")
            pip_audit_args.append(input_)
        else:
            if not input_.is_file():
                _fatal_help(f"input {input_} does not look like a file")
            pip_audit_args.extend(["--requirement", input_])

print(f"would have run: {pip_audit_args=}")
