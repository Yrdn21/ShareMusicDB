from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enums.SongStatus import SongStatus



if TYPE_CHECKING:
    from models.album import AlbumID


class SongBase(SQLModel):
    name: str
    album_id: int
    status: SongStatus = SongStatus.ACTIVE


class SongID(SongBase, table=True):
    song_id: Optional[int] = Field(default=None, primary_key=True)
    album_id: int = Field(foreign_key="albumid.album_id")
    track_number: int = Field(default = 1)

    album: Optional["AlbumID"] = Relationship(back_populates="songs")

    @property
    def album_track_id(self):
        return f"{self.album_id}-{self.track_number}"