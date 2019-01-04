from formats import money, percentage


class Mortgage(object):

    @classmethod
    def create(cls, loan: float, annual_interest_rate: float, amortization_period: int, annual_payment_count: int):
        """
        :param loan: e.g., 400,000
        :param annual_interest_rate: e.g., 0.03
        :param amortization_period: e.g., 10, 15, 20, 25 and etc.
        :param annual_payment_count: e.g., 12 (monthly), 24 (by-monthly), or 26 (bi-weekly)
        """
        payment_count = amortization_period * annual_payment_count
        interest_rate = annual_interest_rate / annual_payment_count
        payment = loan * interest_rate / (1 - pow(1 + interest_rate, -payment_count))

        interest_payments = []
        principal_payments = []
        remaining_principles = []

        principle = loan
        for i in range(payment_count):
            interest_payment = principle * interest_rate
            principal_payment = payment - interest_payment
            principle = principle * (1 + interest_rate) - payment

            interest_payments.append(interest_payment)
            principal_payments.append(principal_payment)

            remaining_principles.append(principle)

        remaining_principles_by_year = []
        for i in range(amortization_period):
            remaining_principles_by_year.append(remaining_principles[(i + 1) * annual_payment_count - 1])

        return Mortgage(loan, remaining_principles, annual_interest_rate, annual_payment_count,
                        remaining_principles_by_year, amortization_period, interest_payments, principal_payments,
                        payment)

    def __init__(self, loan, remaining_principles, annual_interest_rate, annual_payment_count,
                 remaining_principles_by_year, amortization_period, interest_payments, principal_payments, payment):
        self.loan = loan
        self.remaining_principles = remaining_principles
        self.annual_interest_rate = annual_interest_rate
        self.annual_payment_count = annual_payment_count
        self.remaining_principles_by_year = remaining_principles_by_year
        self.amortization_period = amortization_period
        self.interest_payments = interest_payments
        self.principal_payments = principal_payments
        self.payment = payment

    @property
    def yearly_payment(self):
        return self.payment * self.annual_payment_count

    @property
    def total_payment(self):
        return self.yearly_payment * self.amortization_period

    @property
    def interest_payments_by_year(self):
        return self.group_by_year(values=self.interest_payments)

    @property
    def principal_payments_by_year(self):
        return self.group_by_year(values=self.principal_payments)

    @property
    def description(self):
        return f'The total loan of the mortgage is {money(self.loan)} with ' \
            f'an annual interest rate of {percentage(self.annual_interest_rate)}. ' \
            f'The mortgage term is set to {self.amortization_period} years. ' \
            f'Total mortgage payment is {money(self.total_payment)}. ' \
            f'Monthly payment is {money(self.principal_payments[0] + self.interest_payments[0])}. ' \
            f'For the first month, the principle payment is {money(self.principal_payments[0])}, ' \
            f'and the interest payment is {money(self.interest_payments[0])}. ' \
            f'For the last month, the principle payment is {money(self.principal_payments[-1])}, ' \
            f'and interest payment is {money(self.interest_payments[-1])}. '

    @staticmethod
    def group_by_count(values, count):
        grouped_values = [0] * int(len(values) / count)
        for index, value in enumerate(values):
            group_index = int(index / count)
            grouped_values[group_index] = grouped_values[group_index] + value
        return grouped_values

    def group_by_year(self, values):
        return self.group_by_count(values=values, count=self.annual_payment_count)
