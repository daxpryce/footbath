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

