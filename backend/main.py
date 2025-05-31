from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

app = FastAPI(title="DogRoulette API")

# Allow your frontend (localhost:3000 during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy data for now
DOGS = [
    {
        "id": 1,
        "name": "Charlie",
        "breed": "Golden Retriever",
        "location": "New York, NY",
        "age": "2 years",
        "img_url": "https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg",
        "source_url": "https://www.petfinder.com/petdetail/123456"
    },
    {
        "id": 2,
        "name": "Bella",
        "breed": "Corgi",
        "location": "Philadelphia, PA",
        "age": "1 year",
        "img_url": "https://images.dog.ceo/breeds/corgi-cardigan/n02113186_5566.jpg",
        "source_url": "https://www.petfinder.com/petdetail/789012"
    }
]

@app.get("/dogs")
def get_dogs(limit: int = 1, location: Optional[str] = Query(None)):
    """
    Returns a list of adoptable dogs.
    Supports limiting results and optional location-based filtering.
    """
    results = DOGS
    if location:
        results = [dog for dog in results if location.lower() in dog["location"].lower()]
    return results[:limit]
