from enum import Enum
from typing import Optional, List

class Resolver(Enum):
    OMR = "OMR"
    OCR = "OCR"
    HW = "HW"


class Region:
    y1: int
    y2: int
    x1: int
    x2: int
    resolver: Resolver
    image_path: Optional[str]
    extracted_value: Optional[str]

    def __init__(self, y1: int, y2: int, x1: int, x2: int, resolver: Resolver, image_path: Optional[str] = None, extracted_value: Optional[str] = None) -> None:
        self.y1 = y1
        self.y2 = y2
        self.x1 = x1
        self.x2 = x2
        self.resolver = resolver
        self.image_path = image_path
        self.extracted_value = extracted_value

    @staticmethod
    def from_json(data: dict) -> "Region":
        return Region(
            y1=data["y1"],
            y2=data["y2"],
            x1=data["x1"],
            x2=data["x2"],
            resolver=Resolver(data["resolver"]) if "resolver" in data else None,
            image_path=data.get("image_path"),
            extracted_value=data.get("extracted_value")
        )

    def as_tuple(self):
        return (self.y1, self.y2, self.x1, self.x2)

    def iter_regions(self):
        yield self


class ObservationField:
    index: int
    label_region: Region
    value_region: Region
    s_region: Region
    p_region: Region
    r_region: Region

    def __init__(self, index: int, label_region: Region, value_region: Region, s_region: Region, p_region: Region, r_region: Region) -> None:
        self.index = index
        self.label_region = label_region
        self.value_region = value_region
        self.s_region = s_region
        self.p_region = p_region
        self.r_region = r_region

    @staticmethod
    def from_json(data: dict) -> "ObservationField":
        index = data["index"]
        label_region = Region.from_json(data["label_region"])
        value_region = Region.from_json(data["value_region"])
        s_region = Region.from_json(data["s_region"])
        p_region = Region.from_json(data["p_region"])
        r_region = Region.from_json(data["r_region"])
        return ObservationField(index, label_region, value_region, s_region, p_region, r_region)

    def to_json(self) -> dict:
        return {
            "index": self.index,
            "label": self.label_region.extracted_value,
            "value": self.value_region.extracted_value,
            "s": self.s_region.extracted_value,
            "p": self.p_region.extracted_value,
            "r": self.r_region.extracted_value
        }

    def iter_regions(self):
        yield from self.label_region.iter_regions()
        yield from self.value_region.iter_regions()
        yield from self.s_region.iter_regions()
        yield from self.p_region.iter_regions()
        yield from self.r_region.iter_regions()

class FullObservationField:
    index: int
    label_region: Region
    concern_region: Region
    injury_region: Region
    alternative_region: Region
    s_region: Region
    p_region: Region
    r_region: Region

    def __init__(self, index: int, label_region: Region, concern_region: Region, injury_region: Region, alternative_region: Region, s_region: Region, p_region: Region, r_region: Region) -> None:
        self.index = index
        self.label_region = label_region
        self.concern_region = concern_region
        self.injury_region = injury_region
        self.alternative_region = alternative_region
        self.s_region = s_region
        self.p_region = p_region
        self.r_region = r_region

    @staticmethod
    def from_json(data: dict) -> "FullObservationField":
        index = data["index"]
        label_region = Region.from_json(data["label_region"])
        concern_region = Region.from_json(data["concern_region"])
        injury_region = Region.from_json(data["injury_region"])
        alternative_region = Region.from_json(data["alternative_region"])
        s_region = Region.from_json(data["s_region"])
        p_region = Region.from_json(data["p_region"])
        r_region = Region.from_json(data["r_region"])
        return FullObservationField(index, label_region, concern_region, injury_region, alternative_region, s_region, p_region, r_region)

    def to_json(self) -> dict:
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
        yield from self.label_region.iter_regions()
        yield from self.concern_region.iter_regions()
        yield from self.injury_region.iter_regions()
        yield from self.alternative_region.iter_regions()
        yield from self.s_region.iter_regions()
        yield from self.p_region.iter_regions()
        yield from self.r_region.iter_regions()


class Field:
    index: Optional[int]
    label_region: Region
    value_region: Region

    def __init__(self, index: Optional[int], label_region: Region, value_region: Region) -> None:
        self.index = index
        self.label_region = label_region
        self.value_region = value_region

    @staticmethod
    def from_json(data: dict) -> "Field":
        # index puede no estar presente
        index = data.get("index")
        label_region = Region.from_json(data["label_region"])
        value_region = Region.from_json(data["value_region"])
        return Field(index, label_region, value_region)

    def to_json(self) -> dict:
        data = {
            "label": self.label_region.extracted_value,
            "value": self.value_region.extracted_value
        }
        if self.index is not None:
            data["index"] = self.index
        return data

    def iter_regions(self):
        yield from self.label_region.iter_regions()
        yield from self.value_region.iter_regions()


class FieldGroup:
    label_region: Region
    options: List[Field]

    def __init__(self, label_region: Region, options: List[Field]) -> None:
        self.label_region = label_region
        self.options = options

    @staticmethod
    def from_json(data: dict) -> "FieldGroup":
        label_region = Region.from_json(data["label_region"])
        options = [Field.from_json(opt) for opt in data["options"]]
        return FieldGroup(label_region, options)

    def to_json(self) -> dict:
        return {
            "label": self.label_region.extracted_value,
            "options": [opt.to_json() for opt in self.options]
        }

    def iter_regions(self):
        yield from self.label_region.iter_regions()
        for opt in self.options:
            yield from opt.iter_regions()