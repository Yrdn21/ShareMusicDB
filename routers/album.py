from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from fastapi.responses import RedirectResponse
from models.album import AlbumBase, AlbumRead, AlbumEditionUpdate
from data.db import operations_db
from data.image_storage import save_image
from enums.genre import Genre
from enums.editions import Edition
from typing import Optional


router = APIRouter(prefix="/albums", tags=["Albums"])


@router.post("/", status_code=status.HTTP_303_SEE_OTHER, response_class=RedirectResponse)
def create_album(
    title: str = Form(...),
    artist_id: int = Form(...),
    genre: Genre = Form(...),
    release_year: int = Form(...),
    edition: Edition = Form(Edition.STANDARD),
    cover: Optional[UploadFile] = File(None)
):
    cover_url = save_image(cover, folder="albums") if (cover and cover.filename) else None
    new_album = AlbumBase(
        title=title,
        artist_id=artist_id,
        genre=genre,
        release_year=release_year,
        edition=edition,
        image_url=cover_url
    )
    created = operations_db.create_album_db(new_album)
    if not created:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist ID not found")
    return RedirectResponse(url="/albums", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/show", status_code=status.HTTP_200_OK, response_model=list[AlbumRead], response_description="Showing all albums")
def show_all_albums():
    return operations_db.show_all_albums_db()


@router.get("/history", status_code=status.HTTP_200_OK, response_model=list[AlbumRead], response_description="Showing deleted albums")
def show_deleted_albums():
    return operations_db.show_all_deleted_albums_db()


@router.get("/search", status_code=status.HTTP_200_OK, response_model=AlbumRead, response_description="Showing the album with the matching name")
def show_one_album_by_name(album_name: str):
    album = operations_db.show_one_album_by_name_db(album_name)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No album found")
    return album


@router.get("/{album_id}", status_code=status.HTTP_200_OK, response_model=AlbumRead, response_description="Showing the album with the matching id")
def show_one_album(album_id: int):
    album = operations_db.show_one_album_db(album_id)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No album found")
    return album


@router.patch("/{album_id}/edition", status_code=status.HTTP_200_OK, response_model=AlbumRead, response_description="The edition of the album has been updated")
def update_album_edition(album_id: int, new_edition: AlbumEditionUpdate):
    update = operations_db.update_album_edition_db(album_id, new_edition)
    if not update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return update


@router.delete("/{album_id}/deletealbum", status_code=status.HTTP_200_OK, response_model=AlbumRead, response_description="The album has been deleted")
def delete_album(album_id: int):
    delete = operations_db.delete_album_db(album_id)
    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return delete