from fastapi import FastAPI, Request
import requests
import os
from urllib.parse import quote

app = FastAPI()

API_KEY = os.getenv("EIRCODE_KEY")

@app.post("/api/main")
async def extract_and_lookup(request: Request):
    payload = await request.json()

    if not API_KEY:
        return {"success": False, "message": "API key not loaded"}

    # Step 1: extract eircode
    try:
        eircode = payload["AddressDetails"]["eircode"]
    except KeyError:
        return {"success": False, "message": "eircode not found"}

    try:
        # Step 2: first API call (get ecad_id)
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

        # Step 3: encode ecad_id for URL
        encoded_ecad = quote(ecad_id, safe="")

        # Step 4: second API call
        url_2 = f"https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses/{encoded_ecad}/gbr"
        params_2 = {
            "api_key": API_KEY
        }

        response_2 = requests.get(url_2, params=params_2, timeout=10)
        response_2.raise_for_status()
        data_2 = response_2.json()

        addresses = data_2.get("result", {}).get("addresses", [])
        if not addresses:
            return {"success": False, "message": "No address details found"}
        
        small_area_id = addresses[0].get("small_area_id")

    except Exception as e:
        return {"success": False, "message": str(e)}

    return {
        "success": True,
        "eircode": eircode,
        "ecad_id": ecad_id,
        "small_area_id": small_area_id
    }
