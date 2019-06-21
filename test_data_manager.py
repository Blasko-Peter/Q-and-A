import data_manager
import unittest


class TestDataManager(unittest.TestCase):


    def test_sql_display1(self):
        data = data_manager.sql_display()
        self.assertIsNotNone(data)

    # is true if number of records eqauls 6
    def test_sql_display2(self):
        data = data_manager.sql_display()
        result = len(data)
        self.assertEqual(result, 6)


    def test_sql_display_limit(self):
        data = data_manager.sql_display_limit(3)
        result = len(data)
        self.assertEqual(result, 3)

    # def test_sql_add(self):
    #     subtime = "2019.06.21 21:17:00"
    #     title = "practice"
    #     msg = "this is a good excercise"
    #     img = None
    #     data = data_manager.sql_display()
    #     control_number = len(data) + 1
    #     data_manager.sql_add(subtime, title, msg, img)
    #     result = len(data_manager.sql_display())
    #     self.assertEqual(result, control_number)


    # if you run the test_data_manager please add 1 to data_manager_sql(number)
    # def test_sql_delete(self):
    #     data = data_manager.sql_display()
    #     control_number = len(data) - 1
    #     data_manager.sql_delete(14)
    #     result = len(data_manager.sql_display())
    #     self.assertEqual(result, control_number)


    def test_sql_search1(self):
        data = data_manager.sql_search("dog")
        result = len(data)
        self.assertEqual(result, 1)


    def test_sql_search2(self):
        data = data_manager.sql_search("monkey")
        result = len(data)
        self.assertEqual(result, 1)


    def test_sql_display_question(self):
        data = data_manager.sql_display_question(1)
        result = len(data)
        self.assertEqual(result, 1)


    def test_sql_display_answer(self):
        data = data_manager.sql_display_answer(1)
        result = len(data)
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
