import asyncio
from collections.abc import AsyncIterable
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
from sse_starlette.sse import EventSourceResponse
import time
from services.llm import response

router = APIRouter()

@router.get("/llm/stream", response_class=StreamingResponse)
async def llm_stream() -> AsyncIterable[str]:
    llm_response = response()
    for line in llm_response.splitlines():
        yield json.dumps(line) + '\n'
        time.sleep(.1)

