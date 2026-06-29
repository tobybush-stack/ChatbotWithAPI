import asyncio
from collections.abc import AsyncIterable, Iterable
from fastapi import BackgroundTasks, FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from sse_starlette.sse import EventSourceResponse
import time
from typing import List
from services.providers import Provider, providers_list, provider_insert, providers_sse_generator, provider_generator, providers_load

router = APIRouter()

@router.get("/providers", response_model=List[Provider])
async def get_providers():
    """Get all providers"""
    provider_list = await providers_list()
    return provider_list

@router.post("/provider")
async def post_provider(provider: Provider):
    """Add provider"""
    provider_dict = provider.model_dump()
    provider_insert(provider_dict)
    return provider_dict

@router.get("/providers/stream", response_model=None)
async def providers_stream():
    """Get all providers stream"""
    provider_generator()

@router.get("/providers/sse", response_model=None)
async def providers_sse():
    """Get providers server-side event"""
    return EventSourceResponse(providers_sse_generator())

@router.post("/providers/background_task", status_code=201)
async def load_providers_background(providers: list[Provider], background_tasks: BackgroundTasks):
    """Background task for getting providers"""
    background_tasks.add_task(providers_load, providers)
    return {"message": "Loading providers to database..."}
