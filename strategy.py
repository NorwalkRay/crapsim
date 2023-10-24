from abc import ABC, abstractmethod

'''
Abstract class that represents methods all strategies should have.
'''
class Strategy(ABC):
    
    @abstractmethod
    def get_bets(self, bet_table, point):
        # Returns a dict of bets to be placed
        pass

    @abstractmethod
    def reset(self):
        # Resets the progression of a strategy
        pass

'''
This is an instance of the Strategy abstract class. The strategy will define how to bet over the course of a craps session
(it persists across games). The strategy will take the game state as an input and use the strategy logic to output what bets
should be made.
'''
class Hedge68_Strategy(Strategy):
    
    def __init__(self):
        self.base_pass_line_bet = 25
        self.base_place_bet = 60
        self.base_hardway_bet = 25
        self.pass_line_winner_count = 0
        self.hardway_winner_count = 0

        self.bets_by_point = { # the guts of the strategy
            None: [('PASS_LINE', self.base_pass_line_bet)],
            4: [('PASS_LINE', self.base_pass_line_bet), 
                ('ODD_4', self.base_pass_line_bet * 3), 
                ('PLACE_6', self.base_place_bet),
                ('PLACE_8', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
            5: [('PASS_LINE', self.base_pass_line_bet), 
                ('ODD_5', self.base_pass_line_bet * 4),
                ('PLACE_6', self.base_place_bet),
                ('PLACE_8', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
            6: [('PASS_LINE', self.base_pass_line_bet),
                ('ODD_6', self.base_pass_line_bet * 5),
                ('PLACE_8', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
            8: [('PASS_LINE', self.base_pass_line_bet),
                ('ODD_8', self.base_pass_line_bet * 5),
                ('PLACE_6', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
            9: [('PASS_LINE', self.base_pass_line_bet),
                ('ODD_9', self.base_pass_line_bet * 4),
                ('PLACE_6', self.base_place_bet),
                ('PLACE_8', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
            10: [('PASS_LINE', self.base_pass_line_bet),
                ('ODD_10', self.base_pass_line_bet * 3),
                ('PLACE_6', self.base_place_bet),
                ('PLACE_8', self.base_place_bet),
                ('HARD_6', self.base_hardway_bet),
                ('HARD_8', self.base_hardway_bet)],
        }

    def get_bets(self, bet_table, point):
        new_bets = {}
        for bet_name, bet_amount in self.bets_by_point.get(point, []):
            if bet_table.get_bet_amount(bet_name) == 0:
                new_bets[bet_name] = bet_amount
        return new_bets
    
    def reset(self):
        self.pass_line_winner_count = 0
        self.hardway_winner_count = 0
