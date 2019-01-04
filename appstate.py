from investments import PropertyValue, RentingCapital
from mortgage import Mortgage
from rent import Rent
import json


class AppState:
    def __init__(self, number_of_years, mortgage, renting_capital, property_value, rent, *args, **kwargs):
        self.property_value = property_value
        self.renting_capital = renting_capital
        self.mortgage = mortgage
        self.number_of_years = number_of_years
        self.rent = rent

    @property
    def x_axis_years(self):
        return list(range(1, self.number_of_years + 1))

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(
            property_value=PropertyValue(**json_data["property_value"]),
            renting_capital=RentingCapital(**json_data["renting_capital"]),
            mortgage=Mortgage(**json_data["mortgage"]),
            number_of_years=json_data["number_of_years"],
            rent=Rent(**json_data["rent"])
        )

    def dump(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
