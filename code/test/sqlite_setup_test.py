import unittest
import sqlite3
import sqlite_setup

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        sqlite_setup.create_table(self.conn)

    def test_new_table(self): # These three tests check for the table existence
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='new_table'")
        self.assertIsNotNone(cursor.fetchone())

    def test_account_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Account'")
        self.assertIsNotNone(cursor.fetchone())

    def test_alerts_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Alerts'")
        self.assertIsNotNone(cursor.fetchone())

    def test_account_insert(self): # This test checks for the data in the table
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Account WHERE userId = 1")
        account = cursor.fetchone()
        self.assertIsNotNone(account)
        self.assertEqual(account[1], 'password123')
        self.assertEqual(account[2], 1)  
        self.assertEqual(account[3], '2024-03-02')  
        self.assertEqual(account[4], 0)

    def test_alerts_insert(self): # This test checks for the data in the table
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Alerts")
        self.assertIsNotNone(cursor.fetchone())

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()