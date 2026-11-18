from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import Optional
from models.artist import ArtistID, ArtistBase
from data.db import artist_operations_db as ops
from data.image_storage import save_image, delete_image
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="/artist", tags=["Artist"])


@router.post("/", status_code=status.HTTP_303_SEE_OTHER, response_class=RedirectResponse)
def create_artist(
    name: str = Form(...),
    country: str = Form("Desconocido"),
    image: Optional[UploadFile] = File(None)
):
    image_url = save_image(image, folder="artists") if (image and image.filename) else None
    artist_data = ArtistBase(name=name, country=country, image_url=image_url)
    ops.create_artist_db(artist_data)
    return RedirectResponse(url="/artists", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/show", status_code=status.HTTP_200_OK, response_model=list[ArtistID], response_description="Showing all artists")
def show_all_artist():
    return ops.show_all_artist_db()


@router.get("/search", status_code=status.HTTP_200_OK, response_model=ArtistID, response_description="Showing the artist with the matching name")
def show_one_artist_by_name(artist_name: str):
    artist = ops.show_artist_by_name_db(artist_name)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No artists found")
    return artist


@router.get("/{artist_id}", status_code=status.HTTP_200_OK, response_model=ArtistID, response_description = "Showing the artist with the matching id")
def show_one_artist_by_id(artist_id: int):
    artist = ops.show_one_artist_db(artist_id)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No artists found")
    return artist


@router.patch("/{artist_id}/update", status_code=status.HTTP_200_OK, response_model=ArtistID, response_description = "The artist was updated")
def update_artist(
    artist_id: int,
    name: str = Form(...),
    country: str = Form("Desconocido"),
    image: Optional[UploadFile] = File(None)):
    current_artist = ops.show_one_artist_db(artist_id)
    if not current_artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No artists found")

    image_url = current_artist.image_url
    if image:
        if current_artist.image_url:
            delete_image(current_artist.image_url)
        image_url = save_image(image, folder="artists")

    artist_data = ArtistBase(name=name, country=country, image_url=image_url)
    return ops.update_artist_db(artist_id, artist_data)



@router.delete("/{artist_id}/deleteartist", status_code=status.HTTP_200_OK, response_model=ArtistID, response_description="The artist has been deleted")
def delete_artist(artist_id: int):
    deleted = ops.delete_artist_db(artist_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No artists found")
    if deleted.image_url:
        delete_image(deleted.image_url)
    return deleted