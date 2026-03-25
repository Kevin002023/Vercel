from fastapi import FastAPI
from fastapi import Request

app = FastAPI()

@app.post("/api/main")
async def root(request: Request):
    payload = await request.json()
    return {
        "success": True,
        "message": "Vercel app is working",
        "received": payload
    }
