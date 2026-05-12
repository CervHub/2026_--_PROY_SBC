
"""
Modelos base para extracción de contenido.
Incluye definiciones de Region y BaseField.
"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass

class Resolver(Enum):
    """
    Tipos de resolutores para extracción de datos en regiones.
    """
    OMR = "OMR"
    OCR = "OCR"
    HW = "HW"


@dataclass
class Region:
    """
    Representa una región rectangular en un documento, con información de posición y extracción.

    Args:
        y1 (int): Coordenada superior.
        y2 (int): Coordenada inferior.
        x1 (int): Coordenada izquierda.
        x2 (int): Coordenada derecha.
        resolver (Resolver): Tipo de resolutor (OMR, OCR, HW).
        image_path (Optional[str]): Ruta de la imagen asociada.
        extracted_value (Optional[str]): Valor extraído.
        fixed_value (Optional[str]): Valor corregido.
    """
    y1: int
    y2: int
    x1: int
    x2: int
    resolver: Resolver
    image_path: Optional[str] = None
    extracted_value: Optional[any] = None
    fixed_value: Optional[str] = None


    @staticmethod
    def from_json(data: dict) -> "Region":
        """
        Crea una instancia de Region a partir de un diccionario JSON.
        """
        return Region(
            y1=data["y1"],
            y2=data["y2"],
            x1=data["x1"],
            x2=data["x2"],
            resolver=Resolver(data["resolver"]) if "resolver" in data else None,
            image_path=data.get("image_path"),
            extracted_value=data.get("extracted_value"),
            fixed_value=data.get("fixed_value")
        )


    def as_tuple(self):
        """
        Devuelve la región como una tupla de coordenadas.
        """
        return (self.y1, self.y2, self.x1, self.x2)


    def iter_regions(self):
        """
        Iterador que retorna la propia región.
        """
        yield self


@dataclass
class BaseField:
    """
    Clase base para todos los campos de extracción.
    """
    pass
