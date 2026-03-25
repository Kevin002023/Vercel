from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

API_KEY = os.getenv("EIRCODE_KEY")

@app.get("/")
def home():
    return {"success": True, "message": "Home route is working"}

@app.get("/api/health")
def health():
    return {"success": True, "message": "Health route is working"}

@app.post("/api/main")
async def extract_and_lookup(request: Request):
    payload = await request.json()

    if not API_KEY:
        return {"success": False, "message": "API key not loaded"}

    try:
        eircode = payload["AddressDetails"]["eircode"]
    except KeyError:
        return {"success": False, "message": "eircode not found"}

    url = "https://api.ideal-postcodes.co.uk/v1/autocomplete/addresses"
    params = {
        "q": eircode,
        "api_key": API_KEY,
        "context": "irl",
        "language": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        hits = data.get("result", {}).get("hits", [])
        if not hits:
            return {"success": False, "message": "No address found"}

        ecad_id = hits[0]["id"]

        return {
            "success": True,
            "eircode": eircode,
            "ecad_id": ecad_id
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
