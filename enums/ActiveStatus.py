from enum import Enum, auto

class ActiveStatus(str, Enum):
    AVAILABLE = "Stock Disponible"
    OUT_OF_STOCK = "Sin stock"
