from sqlmodel import Session, select
from models.artist import ArtistID, ArtistBase
from .album import engine
from enums.ArtistStatus import ArtistStatus


def create_artist_db(new_artist: ArtistBase):
    with Session(engine) as session:
        artist_db = ArtistID.model_validate(new_artist)
        artist_db.status = ArtistStatus.ACTIVE
        session.add(artist_db)
        session.commit()
        session.refresh(artist_db)
        return artist_db

def show_all_artist_db(include_inactive: bool = False, only_inactive: bool = False):
    with Session(engine) as session:
        statement = select(ArtistID)
        if only_inactive:
            statement = statement.where(ArtistID.status == ArtistStatus.INACTIVE)
        elif not include_inactive:
            statement = statement.where(ArtistID.status == ArtistStatus.ACTIVE)
        return session.exec(statement).all()


def show_one_artist_db(artist_id: int):
    with Session(engine) as session:
        return session.get(ArtistID, artist_id)

def show_artist_by_name_db(artist_name: str):
    with Session(engine) as session:
        statement = select(ArtistID).where(ArtistID.name.ilike(artist_name))
        return session.exec(statement).first()


def search_artists_db(query: str, status_filter: str = "all"):
    cleaned = query.strip()

    with Session(engine) as session:
        statement = select(ArtistID)

        if status_filter == "inactive":
            statement = statement.where(ArtistID.status == ArtistStatus.INACTIVE)
        elif status_filter == "active":
            statement = statement.where(ArtistID.status == ArtistStatus.ACTIVE)

        if cleaned:
            if cleaned.isdigit():
                statement = statement.where(ArtistID.artist_id == int(cleaned))
            else:
                statement = statement.where(ArtistID.name.ilike(f"%{cleaned}%"))

        return session.exec(statement).all()


def update_artist_db(artist_id: int, update_artist: ArtistBase):
    with Session(engine) as session:
        artist_db = session.get(ArtistID, artist_id)
        if not artist_db:
            return None
        artist_db.name = update_artist.name
        artist_db.country = update_artist.country
        if update_artist.image_url is not None:
            artist_db.image_url = update_artist.image_url
        session.add(artist_db)
        session.commit()
        session.refresh(artist_db)
        return artist_db

def delete_artist_db(artist_id: int):
    with Session(engine) as session:
        artist_db = session.get(ArtistID, artist_id)
        if not artist_db:
            return None
        artist_db.status = ArtistStatus.INACTIVE
        session.add(artist_db)
        session.commit()
        session.refresh(artist_db)
        return artist_db


def toggle_artist_status_db(artist_id: int):
    with Session(engine) as session:
        artist_db = session.get(ArtistID, artist_id)
        if not artist_db:
            return None
        artist_db.status = (ArtistStatus.INACTIVE if artist_db.status == ArtistStatus.ACTIVE else ArtistStatus.ACTIVE)
        session.add(artist_db)
        session.commit()
        session.refresh(artist_db)
        return artist_db