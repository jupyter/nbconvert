"""pytest configuration."""
import asyncio
import faulthandler
import os

faulthandler.enable()

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type:ignore
