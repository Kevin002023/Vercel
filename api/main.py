from fastapi import FastAPI

app = FastAPI()

@app.get("/api/main")
def root():
    return {"success": True, "message": "Vercel app is working"}
