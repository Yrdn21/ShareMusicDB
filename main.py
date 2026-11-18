from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import album, artist, songs

from data.db.album import create_db_tables
from data.image_storage import IMAGES_DIR

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield

app = FastAPI(lifespan=lifespan, title="ShareMusic")
app.mount(IMAGES_URL, StaticFiles(directory=IMAGES_DIR), name="images")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(album.router)
app.include_router(artist.router)
app.include_router(songs.router)