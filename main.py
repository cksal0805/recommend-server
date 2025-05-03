from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from places import get_nearby_restaurants
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
async def recommend_restaurant(
    lat: float = Query(...), lng: float = Query(...)
):
    restaurants = await get_nearby_restaurants(lat, lng)
    if not restaurants:
        return {"message": "No restaurants found."}
    pick = random.choice(restaurants)
    return {
        "name": pick["place_name"],
        "address": pick.get("road_address_name") or pick.get("address_name", "주소 없음")
        
    }
