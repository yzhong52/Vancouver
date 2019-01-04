from formats import money, percentage
from helpers import inflate_value
import json


class Rent(object):

    @classmethod
    def create_rent(cls, initial_monthly_rent, inflation_rate, number_of_years):
        yearly_payments = inflate_value(initial_monthly_rent * 12, inflation_rate=inflation_rate, count=number_of_years)
        return Rent(inflation_rate=inflation_rate, yearly_payments=yearly_payments)

    def __init__(self, inflation_rate, yearly_payments, *args, **kwargs):
        self.inflation_rate = inflation_rate
        self.yearly_payments = yearly_payments

    @property
    def total_payment(self):
        return sum(self.yearly_payments)

    @property
    def description(self):
        return f"Total rent is {money(self.total_payment)}. " \
            f"The monthly rent for the first year is {money(self.yearly_payments[0] / 12)}. " \
            f"The rent is projected to increase by {percentage(self.inflation_rate)} year over year " \
            "based on the inflation rate. " \
            f"The monthly rent for the last year is about {money(self.yearly_payments[-1] / 12)}. "

    def to_json(self):
        return json.dumps(self.__dict__)
