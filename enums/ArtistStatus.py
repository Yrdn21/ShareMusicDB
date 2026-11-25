from enum import Enum

class ArtistStatus(str, Enum):
    ACTIVE = "Activo"
    INACTIVE = "Inactivo"