from fastapi import FastAPI
from fastapi import Request

app = FastAPI()

@app.post("/api/main")
async def extract_eircode(request: Request):
    payload = await request.json()

    try:
        eircode = payload["AddressDetails"]["eircode"]
    except KeyError:
        return {
            "success": False,
            "message": "eircode not found in payload"
        }

    return {
        "success": True,
        "eircode": eircode
    }
