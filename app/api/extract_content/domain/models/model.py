
"""
Modelo principal para la extracción de contenido, compuesto por campos y observaciones.
"""
from typing import List
from dataclasses import dataclass
from app.api.extract_content.domain.models.base import BaseField 
from app.api.extract_content.domain.models.field import Field, OptionField
from app.api.extract_content.domain.models.observation import ObservationGroup


@dataclass
class Model:
    """
    Modelo general que agrupa campos y observaciones extraídas de un documento.

    Args:
        title (str): Título del modelo/documento.
        version (str): Versión del modelo.
        fields (List[BaseField]): Lista de campos y observaciones.
    """
    title: str
    version: str
    fields: List[BaseField]


    @staticmethod
    def from_json(data: dict) -> "Model":
        """
        Crea una instancia de Model a partir de un diccionario JSON.
        """
        title = data.get("title", "")
        version = data.get("version", "")
        fields: List[BaseField] = []
        for field_data in data.get("fields", []):
            if "field" in field_data:
                fields.append(Field.from_json(field_data["key"], field_data["field"]))
            elif "field_group" in field_data:
                fields.append(OptionField.from_json(field_data["key"], field_data["field_group"]))
            elif "observations" in field_data:
                fields.append(ObservationGroup.from_json(field_data))
        return Model(title, version, fields)


    def to_json(self) -> dict:
        """
        Serializa el modelo a un diccionario JSON.
        """
        fields_json = []
        for field in self.fields:
            if isinstance(field, Field):
                fields_json.append(field.to_json())
            elif isinstance(field, OptionField):
                fields_json.append(field.to_json())
            elif isinstance(field, ObservationGroup):
                fields_json.append(field.to_json())
        return {
            "title": self.title,
            "version": self.version,
            "fields": fields_json
        }


    def iter_regions(self):
        """
        Itera sobre todas las regiones de todos los campos y observaciones del modelo.
        """
        for field in self.fields:
            yield from field.iter_regions()