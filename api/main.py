from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

API_KEY = os.getenv(EIRCODE_KEY)

@app.post("/api/main")
async def extract_and_lookup(request: Request):
    payload = await request.json()

    try:
        eircode = payload["AddressDetails"]["eircode"]
    except KeyError:
        return {
            "success": False,
            "message": "eircode not found in payload"
        }

    # Call Ideal Postcodes API
    try:
        url = "https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses"
        params = {
            "q": eircode,
            "api_key": API_KEY,
            "context": "irl",
            "language": "en"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract first result id
        ecad_id = data["result"]["hits"][0]["id"]

    except Exception as e:
        return {
            "success": False,
            "message": f"API call failed: {str(e)}"
        }

    return {
        "success": True,
        "eircode": eircode,
        "ecad_id": ecad_id
    }
