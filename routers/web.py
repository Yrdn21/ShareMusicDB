from fastapi import APIRouter, Request
from templating import templates
from data.db import artist_operations_db, operations_db
from enums.genre import Genre
from enums.editions import Edition

router = APIRouter(include_in_schema=False)

@router.get("/")
async def index(request: Request):
    albums = operations_db.show_all_albums_db()
    return templates.TemplateResponse(request, "index.html", {"albums": albums})

@router.get("/artists")
async def list_artists(request: Request):
    artists = artist_operations_db.show_all_artist_db()
    return templates.TemplateResponse(request, "artists.html", {"title": "Artistas", "artists": artists})

@router.get("/new_artist")
async def new_artist_form(request: Request):
    return templates.TemplateResponse(request, "new_artist.html", {"title": "Nuevo Artista"})

@router.get("/albums")
async def list_albums(request: Request):
    albums = operations_db.show_all_albums_db()
    return templates.TemplateResponse(request, "albums.html", {"title": "Álbumes", "albums": albums})

@router.get("/new_album")
async def new_album_form(request: Request):
    artists = artist_operations_db.show_all_artist_db()
    return templates.TemplateResponse(
        request,
        "new_album.html",
        {
            "title": "Nuevo Álbum",
            "artists": artists,
            "genres": [e.value for e in Genre],
            "editions": [e.value for e in Edition]
        }
    )