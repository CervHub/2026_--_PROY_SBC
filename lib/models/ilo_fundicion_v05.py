from typing import List
from lib.models.base import Field, FieldGroup, ObservationField


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