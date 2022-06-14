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
    print(f"❌ {msg}", file=sys.stderr)
    subprocess.run(_pip_audit("--help"))
    sys.exit(1)


inputs = [Path(p).resolve() for p in sys.argv[1].split()]
summary = Path(os.getenv("GITHUB_STEP_SUMMARY")).open("a")

# The arguments we pass into `pip-audit` get built up in this list.
pip_audit_args = [
    # The spinner is useless in the CI.
    "--progress-spinner=off",
    # Include full descriptions in the output.
    "--desc",
    # Write the output to this logfile, which we'll turn into the step summary (if configured).
    "--output=/tmp/pip-audit-output.txt",
]

if os.getenv("GHA_PIP_AUDIT_NO_DEPS", "false") != "false":
    pip_audit_args.append("--no-deps")

if os.getenv("GHA_PIP_AUDIT_REQUIRE_HASHES", "false") != "false":
    pip_audit_args.append("--require-hashes")

if (
    service := os.getenv("GHA_PIP_AUDIT_VULNERABILITY_SERVICE", "pypi").lower()
) != "pypi":
    pip_audit_args.extend(["--vulnerability-service", service])

# If inputs is empty, we let `pip-audit` run in "pip source" mode by not
# adding any explicit input argument(s).
# Otherwise, we handle either exactly one project path (a directory)
# or one or more requirements-style inputs (all files).
for input_ in inputs:
    # Forbid things that look like flags. This isn't a security boundary; just
    # a way to prevent (less motivated) users from breaking the action on themselves.
    if str(input_).startswith("-"):
        _fatal_help(f"input {input_} looks like a flag")

    if input_.is_dir():
        if len(inputs) != 1:
            _fatal_help("pip-audit only supports one project directory at a time")
        pip_audit_args.append(input_)
    else:
        if not input_.is_file():
            _fatal_help(f"input {input_} does not look like a file")
        pip_audit_args.extend(["--requirement", input_])

status = subprocess.run(_pip_audit(*pip_audit_args))
if status.returncode == 0:
    print("🎉 pip-audit exited successfully", file=summary)
else:
    print("❌ pip-audit found one or more problems", file=summary)

    with open("/tmp/pip-audit-output.txt", "r") as io:
        print(io.read(), file=summary)
