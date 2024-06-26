from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import scrape, quotes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrape.router)
app.include_router(quotes.router)
