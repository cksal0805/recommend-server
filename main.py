from fastapi import FastAPI, Query
from places import get_nearby_restaurants
import random

app = FastAPI()

@app.get("/recommend")
async def recommend_restaurant(
    lat: float = Query(..., description="위도"), 
    lng: float = Query(..., description="경도")
):
    restaurants = await get_nearby_restaurants(lat, lng)

    if not restaurants:
        return {"message": "주변 식당을 찾을 수 없습니다."}

    pick = random.choice(restaurants)

    return {
        "name": pick.get("place_name"),
        "address": pick.get("road_address_name") or pick.get("address_name", "주소 정보 없음"),
        "category_name": pick.get("category_name").split(">")[-1].strip(),
    }
