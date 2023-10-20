




            


class CrapsGame:
    def __init__(self, initial_bankroll, strategy):
        self.bankroll = initial_bankroll
        self.strategy = strategy
        self.bet_table = BetTable()
        self.point = None
        self.roll_history = []
        self.pnl_by_roll = []

    def place_initial_bets(self):
        self.strategy.initial_bets(self.bet_table)
        self.bankroll -= self.bet_table.get_total_bet()
    
    def point_set_bets(self):
        self.strategy.point_set_bets(self.bet_table, self.point)

    def adjust_for_roll(self, die1, die2):
        self.strategy.adjust_for_roll(self.bet_table, die1, die2, self.roll_history)

    # ... (your other methods here)
    
    def run_game(self):
        self.place_initial_bets()
        die1, die2 = roll_dice()
        roll_sum = die1 + die2
        self.roll_history.append((die1, die2))

        # ... (rest of the logic)
        game_pnl = self.bankroll - self.bankroll # need to fix
        self.pnl_by_roll.append(game_pnl)





