from fastapi import FastAPI, Request
import requests
import os
from urllib.parse import quote
from services.sac_lookup import get_sa2022

app = FastAPI()

API_KEY = os.getenv("EIRCODE_KEY")

@app.post("/api/main")
async def extract_and_lookup(request: Request):
    payload = await request.json()

    if not API_KEY:
        return {"success": False, "message": "API key not loaded"}

    try:
        eircode = payload["AddressDetails"]["eircode"]
    except KeyError:
        return {"success": False, "message": "eircode not found"}

    try:
        url_1 = "https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses"
        params = {
            "q": eircode,
            "api_key": API_KEY,
            "context": "irl",
            "language": "en"
        }

        response_1 = requests.get(url_1, params=params, timeout=10)
        response_1.raise_for_status()
        data_1 = response_1.json()

        hits = data_1.get("result", {}).get("hits", [])
        if not hits:
            return {"success": False, "message": "No address found"}

        ecad_id = hits[0]["id"]

        encoded_ecad = quote(ecad_id, safe="")
        url_2 = f"https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses/{encoded_ecad}/gbr"

        response_2 = requests.get(url_2, params={"api_key": API_KEY}, timeout=10)
        response_2.raise_for_status()
        data_2 = response_2.json()

        result = data_2.get("result", {})
        native = result.get("native", {})

        if not native:
            return {"success": False, "message": "No native address details found"}

        small_area_id = native.get("small_area_id")
        if not small_area_id:
            return {"success": False, "message": "small_area_id not found"}

        sa2022 = get_sa2022(small_area_id)
        if not sa2022:
            return {
                "success": False,
                "message": f"No SA2022 found for small_area_id {small_area_id}"
            }

        payload["AddressDetails"]["ecad_id"] = ecad_id
        payload["AddressDetails"]["small_area_id"] = small_area_id
        payload["AddressDetails"]["SA2022"] = sa2022

        return {
            "success": True,
            "payload": payload
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
