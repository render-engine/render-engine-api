# Contributing to the Render Engine Projects

Render Engine API is a unifying API layer for managing and working with [render-engine][render-engine].
The [CLI][cli], [TUI][tui], and custom tools can use this module as a shared API layer. Please refer to
the main [CONTRIBUTING.md](https://github.com/render-engine/render-engine/blob/main/CONTRIBUTING.md)
for more details on how to contribute.

## Render Engine API Specific Topics

Render Engine API is a `uv` based project. For more information on installing `uv` and using it
please see the [uv documentation](https://docs.astral.sh/uv/#installation). To get started, fork
this repository and check out your fork.

```shell
git clone <url to fork>
```

Once you have checked out the repository, run `uv sync --dev` and then activate the `venv` that was
created:

```shell
uv sync --dev
source .venv/bin/activate
```

Once you have done this you will be in the virtual environment and ready to work. It is recommended
that you do a local, editable install of the API in your virtual environment so that you can easily
work with the changes you have made.

```shell
uv pip install -e .
```

This will allow you to test your changes locally.

[render-engine]: https://github.com/render-engine/render-engine
[cli]: https://github.com/render-engine/render-engine-cli
[tui]: https://github.com/render-engine/render-engine-tui
