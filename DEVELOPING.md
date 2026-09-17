# Development

Working on this project is primarily done via [uv](https://astral.sh/uv). 

`uv` will bootstrap the right version of python for this project (and your development platform) and install the right dependencies (based off the `pyproject.toml file`).

Install `uv` and ensure it is on your path prior to running the following commands in your terminal of choice:

```bash
git clone https://github.com/daxpryce/footbath.git
cd footbath
uv sync --all-groups
```

Dev dependencies include jupyter, ruff, and ty; the former for replaying exploratory scripting, the latter two for code formatting and type checking.

## Exploration
Run jupyter via your terminal: 

```bash
uv run jupyter notebook notebooks
```

This runs the jupyter subcommand 'notebook' from within the `notebooks` subdirectory in the root of this git repository.

## Development Tasks
We use [poethepoet](https://poethepoet.natn.io/index.html) for our common developer tasks. A non-exhaustive list includes:

Code Formatting:
```bash
uv run poe format
```

Linting:
```bash
uv run poe lint
```

Type Checking:
```bash
uv run poe typecheck
```

Typos Checking:
```bash
uv run poe typocheck
```

## Pull Request Checklist
- Make sure you run `uv run poe check` prior to opening the PR; the build fails if you haven't done this first.
- Follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for your PR titles.
- Have tests. We prefer more tests than not, but use your best judgement; we'll let you know if we want more tests.

