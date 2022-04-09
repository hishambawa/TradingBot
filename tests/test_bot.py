from threading import Thread
import unittest
import pandas as pd
from bot import Bot

class BotTest(unittest.TestCase):

    def setUp(self):
        self.bot = Bot('User', 5000, ["A", "AAPL", "GOOG", "FB"])

    def test_run(self):
        thread = Thread(target=self.bot.run)
        thread.start()
        thread.force_stop = True

        self.assertTrue(self.bot.running)

    def test_sma(self):
        data = pd.DataFrame([10,20,30,40,50])
        expected_result = [15,25,35,45]

        sma = self.bot.get_sma(data, 2)
        sma.dropna(inplace=True)
        sma_list = sma[0].tolist()

        self.assertListEqual(sma_list, expected_result)
