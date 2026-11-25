from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from templating import templates
from data.db import artist_operations_db, operations_db, songs_operations_db
from enums.genre import Genre
from enums.editions import Edition
from models.album import AlbumEditionUpdate

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
    return templates.TemplateResponse(request, "albums.html", {"title": "Albumes", "albums": albums})

@router.get("/history")
async def album_history(request: Request):
    deleted_albums = operations_db.show_all_deleted_albums_db()
    return templates.TemplateResponse(request, "history.html", {"title": "Albumes sin stock", "albums": deleted_albums})

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

@router.get("/songs")
async def list_songs(request: Request):
    songs = songs_operations_db.show_all_songs()
    return templates.TemplateResponse(request, "songs.html", {"title": "Songs", "songs": songs})



@router.get("/new_song")
async def new_song_form(request: Request):
    albums = operations_db.show_all_albums_db()
    return templates.TemplateResponse(request, "new_song.html", {"title": "Nuevo Song", "albums": albums})


@router.get("/albums/{album_id}/songs")
async def album_songs_view(request: Request, album_id: int):
    album = operations_db.show_one_album_db(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return templates.TemplateResponse(request, "album_songs.html", {"title": f"Canciones de {album.title}", "album": album, "songs": album.songs})


