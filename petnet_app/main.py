"""PetNet application."""

import logging
import os

from fastapi import FastAPI, Request

logger = logging.getLogger("fastapi")

app = FastAPI()


@app.get("/ping")
async def ping():
    """Ping end-point return PONG."""
    pid = os.getpid()
    return {"pid": pid}


@app.get("/", include_in_schema=False)
async def home(_request: Request):
    """Send the home page."""
    return {"home": "page"}
