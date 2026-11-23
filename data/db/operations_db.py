from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from enums.StockStatus import StockStatus
from models.album import AlbumID, AlbumBase, AlbumEditionUpdate
from models.artist import ArtistID
from .album import engine


def create_album_db(new_album: AlbumBase):
    with Session(engine) as session:
        artist = session.get(ArtistID, new_album.artist_id)
        if not artist:
            return None

        album_db = AlbumID.model_validate(new_album)
        session.add(album_db)
        session.commit()
        session.refresh(album_db)

        _ = album_db.artist
        _ = album_db.songs
        return album_db


def show_all_albums_db():
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.status == StockStatus.AVAILABLE)
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        return session.exec(statement).all()


def show_all_deleted_albums_db():
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.status == StockStatus.AVAILABLE)
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        return session.exec(statement).all()


def show_one_album_db(album_id: int):
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.album_id == album_id)
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        return session.exec(statement).first()


def show_one_album_by_name_db(album_name: str):
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.title.ilike(album_name))
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        return session.exec(statement).first()


def update_album_edition_db(album_id: int, edition_update: AlbumEditionUpdate):
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.album_id == album_id)
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        album_db = session.exec(statement).first()
        if not album_db:
            return None

        album_db.edition = edition_update.edition
        session.add(album_db)
        session.commit()
        session.refresh(album_db)

        _ = album_db.artist
        _ = album_db.songs
        return album_db


def delete_album_db(album_id: int):
    with Session(engine) as session:
        statement = (
            select(AlbumID)
            .where(AlbumID.album_id == album_id)
            .options(selectinload(AlbumID.artist), selectinload(AlbumID.songs))
        )
        album_db = session.exec(statement).first()
        if not album_db:
            return None

        album_db.status = ActiveStatus.INACTIVE
        session.add(album_db)
        session.commit()
        session.refresh(album_db)

        _ = album_db.artist
        _ = album_db.songs
        return album_db