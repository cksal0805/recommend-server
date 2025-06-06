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
    lat: float = Query(...),
    lng: float = Query(...),
    category: str = Query(None)
):
    all_restaurants = await get_nearby_restaurants(lat, lng)

    if category:
        # 리스트 컴프리헨션
        # all_restaurants 리스트 순회하며,
        # 각 식당의 category_name에 파라미터 category가 포함된 경우 리스트에 담음
        filtered = [
            r for r in all_restaurants
            if category in r.get("category_name", "")
        ]
    else:
        filtered = all_restaurants

    if not filtered:
        return {"message": "No restaurants found."}

    pick = random.choice(filtered)
    return {
        "name": pick["place_name"],
        "address": pick.get("road_address_name") or pick.get("address_name", "주소 없음"),
        "category": pick.get("category_name"),
        "place": pick.get("place_url"),
        "x": pick.get("x"),
        "y": pick.get("y")
    }
