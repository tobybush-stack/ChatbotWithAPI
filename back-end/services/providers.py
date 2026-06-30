import asyncio
from models.providers import Provider, providers_table
from fastapi import HTTPException

async def providers_list():
    try:
        await providers_list = list(providers_table)
    except Exception as e:
        raise HTTPException(500, "Failed to get providers due to the following error:\n" + str(e))

    if len(providers_list) == 0:
        raise HTTPException(404, "Failed to get providers because providers table is empty")

async def providers_sse_generator():
    if len(providers_table) == 0:
        raise HTTPException(404, "Failed to get providers using sse because providers table is empty")
    
    for provider in providers_table:
        await asyncio.sleep(.1)
        try:
            yield(provider)
        except Exception as e:
            raise HTTPException(500, "Failed to get provider using sse with id: " + provider.id + " due to the following error:\n" + str(e))

async def provider_insert(provider: Provider):

    provider_id = max([provider.id for provider in providers_table]) + 1
    provider.id = provider_id

    try:
        matching_providers = [provider.name for provider in providers_table.items() if provider.name == provider.name]
    except Exception as e:
        raise HTTPException(500, "Failed to check provider id (for insert) " + provider.id + " due to the following error:\n" + str(e))

    if len(matching_providers) > 0:
        raise HTTPException(400, "Failed to insert provider id " + provider.id + " because provider id is already in use")

    try:
        await providers_table.append(provider)
    except:
        raise HTTPException(500, "Failed to insert provider ")

async def provider_generator():
    if len(providers_table) == 0:
        raise HTTPException(404, "Failed to stream providers with sse because providers table is empty")
    
    for provider in providers_table:
        await asyncio.sleep(.1)
        try:
            yield(provider)
        except Exception as e:
            raise HTTPException(500, "Failed to stream provider with id: " + provider.id + " due to the following error:\n" + str(e))

async def providers_load(providers: list[Provider]):
    provider_id = max([provider.id for provider in providers_table.items()]) + 1
    initial_provider_id = provider_id
    for provider in providers:
        try:
            matching_providers = [provider.name for provider in providers_table if provider.name == provider.name]
        except Exception as e:
            raise HTTPException(500, "Failed to check provider id (for insert) " + provider.id + " due to the following error:\n" + str(e))

        if len(matching_providers) > 0:
            raise HTTPException(400, "Failed to bulk insert providers because because provider id " + provider.id + " is already in use")

        provider.id = provider_id
        provider_id = provider_id + 1
        
        try:
            await providers_table.extend(providers)
        except:
            raise HTTPException(500, "Failed to bulk insert providers for ids " + str(initial_provider_id) + " to " + str(provider_id) + " due to the following error:\n" + str(e))
        

