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

    def to_json(self) -> dict:
        return {
            "y1": self.y1,
            "y2": self.y2,
            "x1": self.x1,
            "x2": self.x2,
            "resolver": self.resolver.value if self.resolver else None,
            "image_path": self.image_path,
            "extracted_value": self.extracted_value
        }

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
            "label_region": self.label_region.to_json(),
            "value_region": self.value_region.to_json(),
            "s_region": self.s_region.to_json(),
            "p_region": self.p_region.to_json(),
            "r_region": self.r_region.to_json()
        }

    def iter_regions(self):
        yield from self.label_region.iter_regions()
        yield from self.value_region.iter_regions()
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
            "label_region": self.label_region.to_json(),
            "value_region": self.value_region.to_json()
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
            "label_region": self.label_region.to_json(),
            "options": [opt.to_json() for opt in self.options]
        }

    def iter_regions(self):
        yield from self.label_region.iter_regions()
        for opt in self.options:
            yield from opt.iter_regions()
            

class IloFundicionV05:
    observer_name: Field
    register: Field
    date: Field
    time: Field
    area: FieldGroup
    department: FieldGroup
    equipment: FieldGroup
    activity: FieldGroup
    activity_detail: Field
    observations: List[ObservationField]
    comment: Field

    def __init__(self, observer_name: Field, register: Field, date: Field, time: Field, area: FieldGroup, department: FieldGroup, equipment: FieldGroup, activity: FieldGroup, activity_detail: Field, observations: List[ObservationField], comment: Field) -> None:
        self.observer_name = observer_name
        self.register = register
        self.date = date
        self.time = time
        self.area = area
        self.department = department
        self.equipment = equipment
        self.activity = activity
        self.activity_detail = activity_detail
        self.observations = observations
        self.comment = comment

    @staticmethod
    def from_json(data: dict) -> "IloFundicionV05":
        observer_name = Field.from_json(data["observer_name"])
        register = Field.from_json(data["register"])
        date = Field.from_json(data["date"])
        time = Field.from_json(data["time"])
        area = FieldGroup.from_json(data["area"])
        department = FieldGroup.from_json(data["department"])
        equipment = FieldGroup.from_json(data["equipment"])
        activity = FieldGroup.from_json(data["activity"])
        activity_detail = Field.from_json(data["activity_detail"])
        observations = [ObservationField.from_json(obs) for obs in data["observations"]]
        comment = Field.from_json(data["comment"])
        return IloFundicionV05(
            observer_name, register, date, time, area, department, equipment, activity, activity_detail, observations, comment
        )

    def to_json(self) -> dict:
        return {
            "observer_name": self.observer_name.to_json(),
            "register": self.register.to_json(),
            "date": self.date.to_json(),
            "time": self.time.to_json(),
            "area": self.area.to_json(),
            "department": self.department.to_json(),
            "equipment": self.equipment.to_json(),
            "activity": self.activity.to_json(),
            "activity_detail": self.activity_detail.to_json(),
            "observations": [obs.to_json() for obs in self.observations],
            "comment": self.comment.to_json()
        }

    def iter_regions(self):
        yield from self.observer_name.iter_regions()
        yield from self.register.iter_regions()
        yield from self.date.iter_regions()
        yield from self.time.iter_regions()
        yield from self.area.iter_regions()
        yield from self.department.iter_regions()
        yield from self.equipment.iter_regions()
        yield from self.activity.iter_regions()
        yield from self.activity_detail.iter_regions()
        for obs in self.observations:
            yield from obs.iter_regions()
        yield from self.comment.iter_regions()