"""Entry point to run the optimizer API locally."""

from __future__ import annotations

import uvicorn


if __name__ == "__main__":
    uvicorn.run("optimizer_api.api:app", host="0.0.0.0", port=8000, reload=False)
