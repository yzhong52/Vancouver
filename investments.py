from mortgage import Mortgage
from formats import money, percentage
from rent import Rent
import helpers


class RentingCapital(object):
    @classmethod
    def create(cls, initial_capital: float, return_on_investment: float, monthly_property_owning_cost: float,
               mortgage, rent: Rent, number_of_years: int):
        current_capital = initial_capital
        inflation_rate = rent.inflation_rate
        yearly_property_owning_costs = helpers.inflate_value(
            initial=monthly_property_owning_cost * 12,
            inflation_rate=inflation_rate,
            count=number_of_years
        )

        capitals = []
        investments = []
        for i in range(0, number_of_years):
            investment = mortgage.yearly_payment + yearly_property_owning_costs[i] - rent.yearly_payments[i]
            if i == 0:
                investments.append(investment + initial_capital)
            else:
                investments.append(investment)

            current_capital = current_capital * (return_on_investment + 1) + investment
            capitals.append(current_capital)

        rent_yearly_payments = rent.yearly_payments
        mortgage_yearly_payment = [mortgage.yearly_payment] * number_of_years

        description = "The cost is normally lower to rent than to buy. " \
            f"With renting, the extra cash can be " \
            f"put towards other investments so that the capital can grow. " \
            f"Firstly of all, this includes the initial cost for buying, e.g., down payment, etc., which is " \
            f"{money(initial_capital)}. " \
            f"Apart from that, the monthly difference between renting and buying " \
            f"should also be taken into account. And the difference for the first year is " \
            f"{money(mortgage.yearly_payment)} (mortgage) + " \
            f"{money(yearly_property_owning_costs[0])} (property tax, condo fee, etc.) - " \
            f"{money(rent.yearly_payments[0])} (rending cost) = " \
            f"{money(mortgage.yearly_payment + yearly_property_owning_costs[0] - rent.yearly_payments[0])}. " \
            f"And similarly, the cost different for the the last year is " \
            f"{money(mortgage.yearly_payment + yearly_property_owning_costs[-1] - rent.yearly_payments[-1])}. "

        return cls(capitals, investments, yearly_property_owning_costs, rent_yearly_payments, mortgage_yearly_payment,
                   description)

    def __init__(
            self,
            capitals,
            investments,
            yearly_property_owning_costs,
            rent_yearly_payments,
            mortgage_yearly_payment,
            description
    ):
        self.capitals = capitals
        self.investments = investments
        self.yearly_property_owning_costs = yearly_property_owning_costs
        self.rent_yearly_payments = rent_yearly_payments
        self.mortgage_yearly_payment = mortgage_yearly_payment
        self.description = description


class PropertyValue(object):
    @classmethod
    def create(cls, initial_value, appreciation_rate, mortgage: Mortgage, number_of_years,
               real_estate_commission: float = 0.05):
        value_by_year = []

        # The value of selling the house at year N
        equity_by_year = []

        current_value = initial_value
        for i in range(number_of_years):
            current_value = current_value * (1 + appreciation_rate)
            value_by_year.append(current_value)

            current_equity = current_value * (1 - real_estate_commission) - mortgage.remaining_principles_by_year[i]
            equity_by_year.append(current_equity)

        return PropertyValue(appreciation_rate,
                             real_estate_commission,
                             initial_value,
                             value_by_year,
                             equity_by_year)

    def __init__(self, appreciation_rate, real_estate_commission, initial_value, value_by_year, equity_by_year,
                 *args, **kwargs):
        self.appreciation_rate = appreciation_rate
        self.real_estate_commission = real_estate_commission
        self.initial_value = initial_value
        self.value_by_year = value_by_year
        self.equity_by_year = equity_by_year

    @property
    def description(self):
        return f"The property is estimated to appreciate {percentage(self.appreciation_rate)} per year. " \
            f"The initial value of the property is {money(self.initial_value)}. " \
            f"By the 25th year, the value of the property is estimated to be {money(self.value_by_year[-1])}. " \
            f"We assume that you will pay {percentage(self.real_estate_commission)} of the sales price " \
            "as commission to real estate agent. " \
            "The total income by selling the property is the value of the property minus the remaining " \
            "mortgage principle to the bank. " \
            f"If you sell the property at the 1st year, you will gain {money(self.equity_by_year[0])}. " \
            f"If you sell the property at the 25th year, you will gain {money(self.equity_by_year[-1])}. "
