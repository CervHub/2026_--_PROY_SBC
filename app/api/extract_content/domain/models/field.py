
"""
Modelos de campos simples y agrupados para extracción de contenido.
"""
from typing import List, Optional
from dataclasses import dataclass
from app.api.extract_content.domain.models.base import BaseField, Region



@dataclass
class Field(BaseField):
    """
    Campo simple con región de etiqueta y valor.

    Args:
        key (str): Identificador del campo.
        index (Optional[int]): Índice del campo (si aplica).
        label_region (Region): Región de la etiqueta.
        value_region (Region): Región del valor.
    """
    key: Optional[str]
    index: Optional[int]
    label_region: Region
    value_region: Region


    @staticmethod
    def from_json(key: Optional[str], data: dict) -> "Field":
        """
        Crea una instancia de Field a partir de un diccionario JSON.
        """
        index = data.get("index")
        label_region = Region.from_json(data["label_region"])
        value_region = Region.from_json(data["value_region"])
        return Field(key, index, label_region, value_region)


    def to_json(self) -> dict:
        """
        Serializa el campo a un diccionario JSON.
        """
        data = {
            "label": self.label_region.extracted_value,
            "value": self.value_region.extracted_value
        }
        if self.key is not None:
            data["key"] = self.key
        if self.index is not None:
            data["index"] = self.index
        return data


    def iter_regions(self):
        """
        Itera sobre las regiones asociadas al campo.
        """
        yield from self.label_region.iter_regions()
        yield from self.value_region.iter_regions()


@dataclass
class OptionField(BaseField):
    """
    Grupo de campos con una región de etiqueta y una lista de opciones (campos).

    Args:
        key (str): Identificador del grupo.
        label_region (Region): Región de la etiqueta del grupo.
        options (List[Field]): Lista de campos dentro del grupo.
    """
    label_region: Region
    options: List[Field]


    @staticmethod
    def from_json(key: Optional[str], data: dict) -> "OptionField":
        """
        Crea una instancia de FieldGroup a partir de un diccionario JSON.
        """
        label_region = Region.from_json(data["label_region"])
        options = [Field.from_json(None, opt) for opt in data["options"]]
        return OptionField(key, label_region, options)


    def to_json(self) -> dict:
        """
        Serializa el grupo de campos a un diccionario JSON.
        """
        return {
            "key": self.key,
            "label": self.label_region.extracted_value,
            "options": [opt.to_json() for opt in self.options]
        }


    def iter_regions(self):
        """
        Itera sobre las regiones asociadas al grupo y sus opciones.
        """
        yield from self.label_region.iter_regions()
        for opt in self.options:
            yield from opt.iter_regions()