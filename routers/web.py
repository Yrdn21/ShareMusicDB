from fastapi import APIRouter, Request, HTTPException, Form, Query
from fastapi.responses import RedirectResponse
from typing import Optional
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
async def list_artists(request: Request, status= Query(default=("all"))):
    if status == "inactive":
        artists = artist_operations_db.show_all_artist_db(only_inactive=True)
    elif status == "active":
        artists = artist_operations_db.show_all_artist_db(include_inactive=False)
    else:
        artists = artist_operations_db.show_all_artist_db(include_inactive=True)

    return templates.TemplateResponse(request, "artists.html", {"title": "Artistas", "artists": artists, "current_status": status,})

@router.get("/new_artist")
async def new_artist_form(request: Request):
    return templates.TemplateResponse(request, "new_artist.html", {"title": "Nuevo Artista"})

@router.get("/albums")
async def list_albums(request: Request, q: Optional[str] = Query(default=(None))):
    if q and q.strip():
        albums = operations_db.search_albums_db(q)
    else:
        albums = operations_db.show_all_albums_db()

    return templates.TemplateResponse(request, "albums.html", {"title": "Albumes", "albums": albums, "editions": [e.value for e in Edition], "search_query": q or ""})

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


@router.post("/albums/{album_id}/edit_edition")
async def update_album_edition_web(album_id: int, edition: Edition = Form(...)):
    update = operations_db.update_album_edition_db(album_id, AlbumEditionUpdate(edition=edition))
    if not update:
        raise HTTPException(status_code=404, detail="Album not found")
    return RedirectResponse("/albums", status_code=303)


@router.post("/artist/{artist_id}/toggle_status")
def web_toggle_artist_status(artist_id: int):
    artist = artist_operations_db.toggle_artist_status_db(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return RedirectResponse(url="/artists", status_code=303)