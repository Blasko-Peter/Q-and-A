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


    def test_sql_display_comment_to_answer1(self):
        data = data_manager.sql_display_comment_to_answer()
        result = len(data)
        self.assertIsNotNone(result)

    # now there are 3 comment to answers
    def test_sql_display_comment_to_answer2(self):
        data = data_manager.sql_display_comment_to_answer()
        result = len(data)
        self.assertEqual(result, 3)

    # this is true only in the basic case
    def test_sql_get_question_comments0(self):
        data = data_manager.sql_get_question_comments(0)
        result = len(data)
        self.assertEqual(result, 1)

    # this is true only in the basic case
    def test_sql_get_question_comments1(self):
        data = data_manager.sql_get_question_comments(1)
        result = len(data)
        self.assertEqual(result, 0)

    # this is true only in the basic case
    def test_sql_get_question_comments2(self):
        data = data_manager.sql_get_question_comments(2)
        result = len(data)
        self.assertEqual(result, 0)


    def test_sql_display_actual_answer(self):
        data = data_manager.sql_display_actual_answer(1)
        result = len(data)
        self.assertEqual(result, 1)


    def test_question_or_answer1(self):
        data = data_manager.question_or_answer(1)
        result = data['question_id']
        self.assertEqual(result, 0)


    def test_question_or_answer2(self):
        data = data_manager.question_or_answer(2)
        result = data['question_id']
        self.assertEqual(result, None)


    def test_get_question_id(self):
        data = data_manager.get_question_id(2)
        result = data['question_id']
        self.assertEqual(result, 1)


    def test_get_comment_data(self):
        data = data_manager.get_comment_data(1)
        result = len(data)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
