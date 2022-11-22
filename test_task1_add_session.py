import datetime
import unittest
import pandas as pd
from task1_add_session import add_session


class TestAddSession(unittest.TestCase):

    def setUp(self):

        # Инициализируем тестовый dataframe
        test_data = {"customer_id": pd.Series([1, 1, 2, 2, 3, 2, 1, 3, 4, 4, 3, 2, 4, 1, 4]),
                     "product_id": pd.Series([7, 8, 9, 6, 7, 8, 9, 6, 7, 8, 9, 6, 6, 6, 7]),
                     "timestamp": pd.Series([datetime.datetime(2022, 11, 22, 13, 0),
                                             datetime.datetime(2022, 11, 22, 13, 2),
                                             datetime.datetime(2022, 11, 22, 13, 3),
                                             datetime.datetime(2022, 11, 22, 13, 10),
                                             datetime.datetime(2022, 11, 22, 13, 12),
                                             datetime.datetime(2022, 11, 22, 13, 13),
                                             datetime.datetime(2022, 11, 22, 13, 14),
                                             datetime.datetime(2022, 11, 22, 13, 19),
                                             datetime.datetime(2022, 11, 22, 13, 24),
                                             datetime.datetime(2022, 11, 22, 13, 25),
                                             datetime.datetime(2022, 11, 22, 13, 26),
                                             datetime.datetime(2022, 11, 22, 13, 27),
                                             datetime.datetime(2022, 11, 22, 13, 29),
                                             datetime.datetime(2022, 11, 22, 13, 36),
                                             datetime.datetime(2022, 11, 22, 13, 37)])}

        self.df = pd.DataFrame(test_data)

        # Инициализируем ожидаемый dataframe
        test_data['session_id'] = pd.Series([0, 0, 2, 3, 4, 3, 6, 7, 8, 8, 10, 11, 12, 13, 14])
        self.exp_df = pd.DataFrame(test_data)

        # Инициализируем неожидаемый dataframe
        test_data['session_id'] = pd.Series([1, 2, 2, 3, 4, 3, 6, 7, 8, 8, 10, 11, 12, 13, 14])
        self.unexp_df = pd.DataFrame(test_data)

    def test_add_session(self):
        result_df = add_session(self.df)
        self.assertTrue(self.exp_df.equals(result_df))
        self.assertFalse(self.unexp_df.equals(result_df))


if __name__ == '__main__':
    unittest.main()
