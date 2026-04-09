import asyncio
from collections.abc import AsyncIterable, Iterable
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import time
from typing import List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Provider(BaseModel):
    id: int
    name: str
    status: str = "Idle"
    location: str | None = None

# db = {
#     1: Provider(id=1, name="General Hospital"),
#     2: Provider(id=2, name="North Clinic"),
#     3: Provider(id=3, name="South Clinic"),
#     4: Provider(id=4, name="Saint James Hospital")
# }

providers_table = [
    Provider(id=1, name="General Hospital"),
    Provider(id=2, name="North Clinic"),
    Provider(id=3, name="South Clinic"),
    Provider(id=4, name="Saint James Hospital")
]

@app.get("/")
async def root():
    return {"message": "root"}

# get list of providers
@app.get("/providers", response_model=List[Provider])
async def get_providers():
    return list(providers_table)

@app.post("/provider")
async def post_provider(provider: Provider):
    provider_dict = provider.model_dump()
    providers_table.append(provider)
    return provider_dict

@app.get("/providers/stream", response_model=None)
async def providers_stream():
    for provider in providers_table:
        yield(provider)

async def providers_sse_generator():
    for provider in providers_table:
        yield(provider)
        time.sleep(.1)

@app.get("/providers/sse", response_model=None)
async def providers_sse():
    return EventSourceResponse(providers_sse_generator())

def load_providers(providers: list[Provider]):
    for provider in providers:
        providers_table.append(provider)

@app.post("/providers/background_task", status_code=201)
async def load_providers_background(providers: list[Provider], background_tasks: BackgroundTasks):
    background_tasks.add_task(load_providers, providers)
    return {"message": "Loading providers to database..."}

llm_response = """
James Bond, code-named 007, is a fictional British Secret Service
(MI6) agent created by author Ian Fleming in 1953. He is a highly
skilled spy with a "license to kill," known for using high-tech
gadgets, driving fast cars, and enjoying martinis. Bond has
appeared in novels and a long-running film franchise.

Key Details About James Bond:
Origin: Created by Ian Fleming in 1953 for the novel Casino Royale.
Role: Commander in the Royal Naval Reserve and Senior Operational
Officer of the Double-O Section at MI6.
Creator: Ian Fleming, a former naval intelligence officer, based the
character on commandos he knew during World War II.
Key Traits: Known for his loyalty to the British Crown, love for luxury items,
gambling, and a "shaken, not stirred" martini.
Film History: The film series began in 1962 with Dr. No, starring Sean Connery.

Actors Who Have Played Bond:
Sean Connery
George Lazenby
Roger Moore
Timothy Dalton
Pierce Brosnan
Daniel Craig
"""

@app.get("/llm/stream", response_class=StreamingResponse)
async def llm_stream() -> AsyncIterable[str]:
    for line in llm_response.splitlines():
        yield json.dumps(line) + '\n'
        time.sleep(.1)

