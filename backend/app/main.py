from fastapi import FastAPI
from app.api import health

app = FastAPI(title="MarketChronicle")
app.include_router(health.router)