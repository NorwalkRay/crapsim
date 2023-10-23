import unittest
from bet_table import BetTable
from utilities import roll_dice
from craps_session import CrapsSession

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


# Mock Strategy class for testing
class MockStrategy:
    def place_initial_bets(self, bet_table, running_bankroll):
        pass
    def place_post_point_bets(self, bet_table, running_bankroll, point):
        pass

class TestCrapsSession(unittest.TestCase):

    def setUp(self):
        self.strategy = MockStrategy()
        self.session = CrapsSession(1000, self.strategy)

    def test_session_initialization(self):
        self.assertEqual(self.session.game_counter, 0)
        self.assertEqual(self.session.roll_history, [])
        self.assertEqual(self.session.running_bankroll, {'amount': 1000})
        self.assertEqual(self.session.point, None)
        self.assertIsInstance(self.session.bet_table, BetTable)
        self.assertIsInstance(self.session.strategy, MockStrategy)

    def test_initial_bet_placement(self):
        self.session.place_initial_bets()
        # Add assertions based on what your initial bets should be
        
    def test_execute_next_roll(self):
        self.session.execute_next_roll()
        # Add assertions based on what the next roll should do
        
    def test_make_payouts(self):
        self.session.make_payouts(5, 6)  # A sum of 11 for example
        # Add assertions based on what the expected payouts should be

    # Strategy-specific test; replace with your actual strategy
    def test_strategy_initial_bet(self):
        self.session.strategy.place_initial_bets(self.session.bet_table, self.session.running_bankroll)
        # Add assertions based on what the strategy's initial bets should be

    # More tests can be added

if __name__ == '__main__':
    unittest.main()