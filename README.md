# Render Engine API - Feature Consolidation Plan

A unifying api for managing and working with [render-engine][render-engine].

## Overview

The [CLI][cli], [TUI][tui], and custom tools can use this module as a shared API layer. This allows us to:

- **Reduce Duplication**: Single source of truth for common operations
- **Improve Maintainability**: Fix bugs and add features in one place
- **Enable New Tools**: Make it easy to build new render-engine tools
- **Better Testing**: Test shared logic once, comprehensively
- **Consistency**: Ensure all tools behave the same way

## Installation

Install `render-engine-api` using [uv][uv]:

```bash
uv add render-engine-api
```

For development:

```bash
uv sync --dev
```

[render-engine]: https://github.com/render-engine/render-rengine
[cli]: https://github.com/render-engine/render-engine-cli
[tui]: https://github.com/render-engine/render-engine-tui
[uv]: https://docs.astral.sh/uv/
