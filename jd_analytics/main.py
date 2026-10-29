
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jd_routes import router

app = FastAPI(title="RADIX JD Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/jd-analytics")


@app.get("/")
def home():
    return {"message": "JD Analytics API is running"}
