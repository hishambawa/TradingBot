import unittest
import app
import json

class Test(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_start(self):
        response = self.app.post("/start", json = {
            "balance" : "5000",
            "symbols" : ["A", "AAPL", "GOOG", "FB"],
            "user" : "User"
        })

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['status'], 1)

    def test_stop(self):
        response = self.app.post("/stop", json = {
            "user" : "User"
        })

        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['status'], 1)

    