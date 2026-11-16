from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enums.genre import Genre
from enums.ActiveStatus import ActiveStatus
from enums.editions import Edition
from models.artist import ArtistBase
from models.songs import SongBase


if TYPE_CHECKING:
    from models.artist import ArtistID
    from models.songs import SongID


class AlbumBase(SQLModel):
    title: str
    artist_id: int
    genre: Genre
    release_year: int
    edition: Edition = Edition.STANDARD
    status: ActiveStatus = ActiveStatus.ACTIVE


class AlbumID(AlbumBase, table=True):
    album_id: Optional[int] = Field(default=None, primary_key=True)
    artist_id: int = Field(foreign_key="artistid.artist_id")

    artist: Optional["ArtistID"] = Relationship(back_populates="albums")
    songs: List["SongID"] = Relationship(back_populates="album")


class AlbumRead(AlbumBase):
    album_id: int
    artist: Optional[ArtistBase] = None
    songs: List[SongBase] = []

class AlbumStatusUpdate(SQLModel):
    status: ActiveStatus


class AlbumEditionUpdate(SQLModel):
    edition: Edition