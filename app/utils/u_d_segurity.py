from abc import ABC
import re


class DataUDSecurity(ABC):
    @staticmethod
    def validate_id(uuid:str):
        if uuid is str:
            raise ValueError("No se admite este tipo de dato.")