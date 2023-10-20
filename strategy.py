from abc import ABC, abstractmethod

# Abstract class that represents methods all strategies should have.
class Strategy(ABC):
    
    @abstractmethod
    def place_initial_bets(self, bet_table):
        pass
    
    @abstractmethod
    def place_post_point_bets(self, bet_table, point):
        pass
    
    @abstractmethod
    def update_bets_after_roll(self, bet_table, die1, die2, roll_history):
        pass

# This is the instance of the specific strategy we're testing. All the strategy logic belongs in here
class Hedge6_Strategy(Strategy):
    
    def __init__(self):
        self.hardway_counter = 0

    def place_initial_bets(self, bet_table):
        bet_table.add_bet('Pass Line', 25)
        
    def place_post_point_bets(self, bet_table, point):
        if point == 4:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
            return (bet_table.get_bet_amount('Pass Line') * 3) + 110
        elif point == 5:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
            return (bet_table.get_bet_amount('Pass Line') * 4) + 110
        elif point == 6:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
            bet_table.add_bet('Place 8', 60)
            bet_table.add_bet('Hard 8', 50)
            bet_table.add_bet('Hard 6', 50)
            return (bet_table.get_bet_amount('Pass Line') * 5) + 160
        elif point == 8:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
            bet_table.add_bet('Hard 8', 50)
            return (bet_table.get_bet_amount('Pass Line') * 5) + 160
        elif point == 9:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
            return (bet_table.get_bet_amount('Pass Line') * 4) + 110
        elif point == 10:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
            return (bet_table.get_bet_amount('Pass Line') * 3) + 110
        else:
            # This should not happen as craps only has points 4, 5, 6, 8, 9, and 10
            raise ValueError("Invalid point value")

    def update_bets_after_roll(self, bet_table, die1, die2, roll_history):
        # no updates to bets after rolls in this strategy
        pass