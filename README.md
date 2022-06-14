gh-action-pip-audit
===================

[![CI](https://github.com/trailofbits/gh-action-pip-audit/actions/workflows/ci.yml/badge.svg)](https://github.com/trailofbits/gh-action-pip-audit/actions/workflows/ci.yml)
[![Self-test](https://github.com/trailofbits/gh-action-pip-audit/actions/workflows/selftest.yml/badge.svg)](https://github.com/trailofbits/gh-action-pip-audit/actions/workflows/selftest.yml)

A GitHub Action that uses [`pip-audit`](https://github.com/trailofbits/pip-audit)
to scan Python dependencies for known vulnerabilities.

## Usage

Simply add `trailofbits/gh-action-pip-audit` to one of your workflows:

```yaml
jobs:
  selftest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: install
        run: pip install .
      - uses: trailofbits/gh-action-pip-audit@v1
```

By default, `pip-audit` will run in "pip source" mode, meaning that it'll
attempt to collect dependencies from the local environment. See
the [configuration](#configuration) documentation below for more input
and behavioral options.

## Configuration

`gh-action-pip-audit` takes a variety of configuration inputs, all of which are
optional.

### `inputs`

**Default**: Empty, indicating "pip source" mode

The `inputs` setting controls what sources `pip-audit` runs on.

To audit one or more requirements-style inputs:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    inputs: requirements.txt dev-requirements.txt
```

To audit a project that uses `pyproject.toml` for its dependencies:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    # NOTE: this can be `.`, for the current directory
    inputs: path/to/project/
```

### `vulnerability-service`

**Default**: `PyPI`

**Options**: `PyPI`, `OSV` (case insensitive)

The `vulnerability-service` setting controls which vulnerability service is used for the audit.
It's directly equivalent to `pip-audit --vulnerability-service=...`.

To audit with OSV instead of PyPI:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    vulnerability-service: osv
```

### `require-hashes`

**Default**: `false`

The `require-hashes` setting controls whether strict hash checking is enabled.
It's directly equivalent to `pip-audit --require-hashes ...`.

Example:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    # NOTE: only works with requirements-style inputs
    inputs: requirements.txt
    require-hashes: true
```

### `no-deps`

**Default**: `false`

The `no-deps` setting controls whether dependency resolution is performed.
It's directly equivalent to `pip-audit --no-deps ...`.

Example:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    # NOTE: only works with requirements-style inputs
    inputs: requirements.txt
    no-deps: true
```

### `summary`

**Default**: `true`

The `summary` setting controls whether a GitHub
[job summary](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/)
is rendered at the end of the action.

Example:

```yaml
- uses: trailofbits/gh-action-pip-audit@v1
  with:
    summary: false
  ```

### Internal options
<details>
  <summary>⚠️ Internal options ⚠️</summary>

  Everything below is considered "internal," which means that it
  isn't part of the stable public settings and may be removed or changed at
  any points. **You probably do not need these settings.**

  All internal options are prefixed with `internal-be-careful-`.

  #### `internal-be-careful-allow-failure`

  **Default**: `false`

  The `internal-be-careful-allow-failure` setting allows the job to pass, even
  if the underlying `pip-audit` run fails (e.g. due to vulnerabilities detected).

  Be very careful with this setting! Using it unwittingly will prevent the action
  from failing your CI when `pip-audit` fails, which is probably not what you want.

  Example:

  ```yaml
  - uses: trailofbits/gh-action-pip-audit@v1
    with:
      internal-be-careful-allow-failure: true
  ```
</details>
