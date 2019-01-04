import unittest
from rent import Rent
import json


class RentTest(unittest.TestCase):

    def test_json_serializable(self):
        rent = Rent.create_rent(initial_monthly_rent=1000, inflation_rate=0.01, number_of_years=25)

        rent_json = json.dumps(rent.__dict__)
        rent_decoded = Rent(**json.loads(rent_json))

        self.assertAlmostEqual(rent_decoded.inflation_rate, rent.inflation_rate)


if __name__ == '__main__':
    unittest.main()
