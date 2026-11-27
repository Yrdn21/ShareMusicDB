from enum import Enum


class SongStatus(str, Enum):
    ACTIVE = "Disponible"
    INACTIVE = "Oculta"