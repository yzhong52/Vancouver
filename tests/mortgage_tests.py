import unittest
from mortgage import Mortgage
import json


class MortgageTest(unittest.TestCase):

    def test_total_payment(self):
        number_of_years = 25
        mortgage = Mortgage(
            loan=400000,
            annual_interest_rate=0.03,
            amortization_period=number_of_years,
            annual_payment_count=12
        )
        total_payment = 0.0025 / (1 - pow(1 + 0.0025, -300)) * 400000 * 300
        self.assertAlmostEqual(mortgage.total_payment, total_payment)

    def test_json_serializable(self):
        mortgage = Mortgage.create(
            loan=400000,
            annual_interest_rate=0.03,
            amortization_period=25,
            annual_payment_count=12
        )
        mortgage_json = json.dumps(mortgage.__dict__)
        mortgage_decoded = Mortgage(**json.loads(mortgage_json))

        self.assertAlmostEqual(mortgage_decoded.loan, mortgage.loan)


if __name__ == '__main__':
    unittest.main()
