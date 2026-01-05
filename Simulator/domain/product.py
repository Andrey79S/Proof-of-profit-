# domain/product.py

from enum import Enum


class ProductState(Enum):
    RAW = "raw"
    PROOFING = "proofing"
    READY = "ready"
    SPOILED = "spoiled"
