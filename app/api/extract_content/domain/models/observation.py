
"""
Modelos de observaciones simples y completas para extracción de contenido.
"""
import abc
from typing import List, Optional
from dataclasses import dataclass
from app.api.extract_content.domain.models.base import BaseField, Region




@dataclass
class ObservationField(BaseField, abc.ABC):
    """
    Clase base abstracta para observaciones.

    Args:
        key (str): Identificador de la observación.
        index (int): Índice de la observación.
        label_region (Region): Región de la etiqueta.
        s_region (Region): Región S.
        p_region (Region): Región P.
        r_region (Region): Región R.
    """
    index: int
    label_region: Region
    s_region: Region
    p_region: Region
    r_region: Region


@dataclass
class SimpleObservationField(ObservationField):
    """
    Observación simple con región de valor.

    Args:
        value_region (Region): Región del valor.
    """
    value_region: Region


    @staticmethod
    def from_json(data: dict) -> "SimpleObservationField":
        """
        Crea una instancia de SimpleObservationField a partir de un diccionario JSON.
        """
        index = data["index"]
        label_region = Region.from_json(data["label_region"])
        value_region = Region.from_json(data["value_region"])
        s_region = Region.from_json(data["s_region"])
        p_region = Region.from_json(data["p_region"])
        r_region = Region.from_json(data["r_region"])
        return SimpleObservationField(None, index, label_region, s_region, p_region, r_region, value_region)


    def to_json(self) -> dict:
        """
        Serializa la observación simple a un diccionario JSON.
        """
        return {
            "index": self.index,
            "label": self.label_region.extracted_value,
            "value": self.value_region.extracted_value,
            "s": self.s_region.extracted_value,
            "p": self.p_region.extracted_value,
            "r": self.r_region.extracted_value
        }


    def iter_regions(self):
        """
        Itera sobre las regiones asociadas a la observación simple.
        """
        yield from self.label_region.iter_regions()
        yield from self.value_region.iter_regions()
        yield from self.s_region.iter_regions()
        yield from self.p_region.iter_regions()
        yield from self.r_region.iter_regions()
        

@dataclass
class FullObservationField(ObservationField):
    """
    Observación completa con regiones de preocupación, lesión y alternativa.

    Args:
        concern_region (Region): Región de preocupación.
        injury_region (Region): Región de lesión.
        alternative_region (Region): Región de alternativa.
    """
    concern_region: Region
    injury_region: Region
    alternative_region: Region


    @staticmethod
    def from_json(data: dict) -> "FullObservationField":
        """
        Crea una instancia de FullObservationField a partir de un diccionario JSON.
        """
        index = data["index"]
        label_region = Region.from_json(data["label_region"])
        concern_region = Region.from_json(data["concern_region"])
        injury_region = Region.from_json(data["injury_region"])
        alternative_region = Region.from_json(data["alternative_region"])
        s_region = Region.from_json(data["s_region"])
        p_region = Region.from_json(data["p_region"])
        r_region = Region.from_json(data["r_region"])
        return FullObservationField(None, index, label_region, s_region, p_region, r_region, concern_region, injury_region, alternative_region)


    def to_json(self) -> dict:
        """
        Serializa la observación completa a un diccionario JSON.
        """
        return {
            "index": self.index,
            "label": self.label_region.extracted_value,
            "concern": self.concern_region.extracted_value,
            "injury": self.injury_region.extracted_value,
            "alternative": self.alternative_region.extracted_value,
            "s": self.s_region.extracted_value,
            "p": self.p_region.extracted_value,
            "r": self.r_region.extracted_value
        }


    def iter_regions(self):
        """
        Itera sobre las regiones asociadas a la observación completa.
        """
        yield from self.label_region.iter_regions()
        yield from self.concern_region.iter_regions()
        yield from self.injury_region.iter_regions()
        yield from self.alternative_region.iter_regions()
        yield from self.s_region.iter_regions()
        yield from self.p_region.iter_regions()
        yield from self.r_region.iter_regions()


@dataclass
class ObservationGroup(BaseField):
    """
    Grupo de observaciones (simples o completas).

    Args:
        key (str): Identificador del grupo.
        observations (List[ObservationField]): Lista de observaciones.
    """
    observations: List['ObservationField']


    @staticmethod
    def from_json(data: dict) -> "ObservationGroup":
        """
        Crea una instancia de ObservationGroup a partir de un diccionario JSON.
        """
        key = data.get("key", "")
        observations = []
        for obs in data.get("observations", []):
            if "value_region" in obs:
                observations.append(SimpleObservationField.from_json(obs))
            elif "concern_region" in obs and "injury_region" in obs and "alternative_region" in obs:
                observations.append(FullObservationField.from_json(obs))
            else:
                raise ValueError("Unknown observation type in JSON")
        return ObservationGroup(key, observations)


    def to_json(self) -> dict:
        """
        Serializa el grupo de observaciones a un diccionario JSON.
        """
        return {
            "key": self.key,
            "observations": [obs.to_json() for obs in self.observations]
        }


    def iter_regions(self):
        """
        Itera sobre las regiones de todas las observaciones del grupo.
        """
        for obs in self.observations:
            yield from obs.iter_regions()