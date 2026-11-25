from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enums.ArtistStatus import ArtistStatus


if TYPE_CHECKING:
    from models.album import AlbumID


class ArtistBase(SQLModel):
    name: str
    country: str = "Desconocido"
    image_url: Optional[str] = None
    status: ArtistStatus = ArtistStatus.ACTIVE


class ArtistID(ArtistBase, table=True):
    artist_id: Optional[int] = Field(default=None, primary_key=True)

    albums: List["AlbumID"] = Relationship(back_populates="artist")