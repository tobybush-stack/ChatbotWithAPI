from fastapi import HTTPException

async def response():
    try:
        await response =  """
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
    except Exception as e:
        raise HTTPException(500, "Failed to generate LLM Streaming Response due to the following error:\n" + str(e))
    return response