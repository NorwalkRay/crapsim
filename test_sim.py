import unittest
from Craps_Sim_v2 import BetTable

class TestBetTable(unittest.TestCase):

    def test_add_bet(self):
        table = BetTable()
        table.add_bet('Pass Line', 25)
        self.assertEqual(table.get_bet_amount('Pass Line'), 25)
        
    def test_get_total_bet(self):
        table = BetTable()
        table.add_bet('Pass Line', 25)
        table.add_bet('Odds', 50)
        self.assertEqual(table.get_total_bet(), 75)

if __name__ == '__main__':
    unittest.main()
