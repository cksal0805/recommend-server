import httpx
import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

async def get_nearby_restaurants(lat: float, lng: float):
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"
    }
    params = {
        "category_group_code": "FD6",  # 음식점
        "x": lng,
        "y": lat,
        "radius": 1000,  # 1000m 이내
        "size": 15,      # 최대 15개
        "sort": "distance"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        print("KAKAO_API_KEY:", KAKAO_API_KEY)
        print("응답 내용:", response.text)
        data = response.json()

        return data.get("documents", [])
