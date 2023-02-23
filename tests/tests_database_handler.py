import unittest
import sys
sys.path.append('./flaskr/')
import app

class TestDatabaseHandler(unittest.TestCase):
    def testAddFunctionality(self):
        databaseHandlerObj = app.DatabaseHandler()
        self.assertEqual(1, 1)
        pass


if __name__ == "__main__":
    unittest.main()