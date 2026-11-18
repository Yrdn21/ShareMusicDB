from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import album, artist, songs, web
from data.db.album import create_db_tables
from data.image_storage import IMAGES_DIR, IMAGES_URL


BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan, title="ShareMusic")

app.mount(IMAGES_URL, StaticFiles(directory=IMAGES_DIR), name="images")


STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


app.include_router(router= web.router, tags=["WEB"])
app.include_router(album.router)
app.include_router(artist.router)
app.include_router(songs.router)