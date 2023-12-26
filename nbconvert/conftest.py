"""pytest configuration."""
import asyncio
import gc
import os

import pytest

if os.name == "nt":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()  # type:ignore[attr-defined]
    )


@pytest.fixture(autouse=True)
def isolate():  # noqa: PT004
    yield
    gc.collect()
