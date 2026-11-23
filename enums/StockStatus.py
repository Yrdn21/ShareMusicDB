from enum import Enum, auto

class StockStatus(str, Enum):
    AVAILABLE = "Stock Disponible"
    OUT_OF_STOCK = "Sin stock"
