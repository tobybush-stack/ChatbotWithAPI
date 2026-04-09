import pytest
from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from main import app, Provider

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "root"}

def test_get_providers():
    response = client.get("/providers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "General Hospital"

def test_post_provider():
    provider = {
        "id": 5,
        "name": "Example Provider Name",
        "status": "Idle"
        }
    response = client.post("/provider", json = provider)
    assert response.json() == {
        "id": 5,
        "name": "Example Provider Name",
        "status": "Idle",
        "location": None
        }

@pytest.mark.asyncio
async def test_providers_stream():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # response = await ac.get("/stream", stream=True)
        response = await ac.get("/providers/stream")
        
        assert response.status_code == 200
        
        content = []
        async for line in response.aiter_lines():
            content.append(line)
        
        expected_content = [
            '{"id": 1, "name": "General Hospital", "status": "Idle", "location": null}',
            '{"id": 2, "name": "North Clinic", "status": "Idle", "location": null}',
            '{"id": 3, "name": "South Clinic", "status": "Idle", "location": null}',
            '{"id": 4, "name": "Saint James Hospital", "status": "Idle", "location": null}',
            '{"id": 5, "name": "Example Provider Name", "status": "Idle", "location": null}',
        ]
        
        assert content == expected_content

def test_provider_sse():
    request = [
        {"id": 6, "name": "Best Clinic", "status": "Idle"},
        {"id": 7, "name": "Value Clinic", "status": "Idle"},
        {"id": 8, "name": "Discount Clinic", "status": "Idle"},
        {"id": 9, "name": "Robotic Clinic", "status": "Idle"}
    ]
    response = client.post("/providers/background_task", json=request)
    assert response.json() == {"message": "Loading providers to database..."}

@pytest.mark.asyncio
async def test_llm_stream():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # response = await ac.get("/stream", stream=True)
        response = await ac.get("/llm/stream")
        
        assert response.status_code == 200
        
        content = []
        async for line in response.aiter_lines():
            content.append(line)
        
        expected_content = [
            '""',
            '"James Bond, code-named 007, is a fictional British Secret Service"',
            '"(MI6) agent created by author Ian Fleming in 1953. He is a highly"',
            '"skilled spy with a \\"license to kill,\\" known for using high-tech"',
            '"gadgets, driving fast cars, and enjoying martinis. Bond has"',
            '"appeared in novels and a long-running film franchise."',
            '""',
            '"Key Details About James Bond:"',
            '"Origin: Created by Ian Fleming in 1953 for the novel Casino Royale."',
            '"Role: Commander in the Royal Naval Reserve and Senior Operational"',
            '"Officer of the Double-O Section at MI6."',
            '"Creator: Ian Fleming, a former naval intelligence officer, based the"',
            '"character on commandos he knew during World War II."',
            '"Key Traits: Known for his loyalty to the British Crown, love for luxury items,"',
            '"gambling, and a \\"shaken, not stirred\\" martini."',
            '"Film History: The film series began in 1962 with Dr. No, starring Sean Connery."',
            '""',
            '"Actors Who Have Played Bond:"',
            '"Sean Connery"',
            '"George Lazenby"',
            '"Roger Moore"',
            '"Timothy Dalton"',
            '"Pierce Brosnan"',
            '"Daniel Craig"',
        ]
        
        assert content == expected_content

