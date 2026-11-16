from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship



if TYPE_CHECKING:
    from models.album import AlbumID


class SongBase(SQLModel):
    name: str
    album_id: int


class SongID(SongBase, table=True):
    song_id: Optional[int] = Field(default=None, primary_key=True)
    album_id: int = Field(foreign_key="albumid.album_id")

    album: Optional["AlbumID"] = Relationship(back_populates="songs")