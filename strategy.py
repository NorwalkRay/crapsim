from abc import ABC, abstractmethod

'''
Abstract class that represents methods all strategies should have.
'''
class Strategy(ABC):
    
    @abstractmethod
    def get_bets(self, betTable, point):
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
        self.basePassLineBet = 25
        self.basePlaceBet = 60
        self.baseHardwayBet = 25
        self.passLineWinnerCount = 0
        self.hardwayWinnerCount = 0

        self.betsByPoint = { # the guts of the strategy
            None: [('PASS_LINE', self.basePassLineBet)],
            4: [('PASS_LINE', self.basePassLineBet), 
                ('ODD_4', self.basePassLineBet * 3), 
                ('PLACE_6', self.basePlaceBet),
                ('PLACE_8', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
            5: [('PASS_LINE', self.basePassLineBet), 
                ('ODD_5', self.basePassLineBet * 4),
                ('PLACE_6', self.basePlaceBet),
                ('PLACE_8', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
            6: [('PASS_LINE', self.basePassLineBet),
                ('ODD_6', self.basePassLineBet * 5),
                ('PLACE_8', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
            8: [('PASS_LINE', self.basePassLineBet),
                ('ODD_8', self.basePassLineBet * 5),
                ('PLACE_6', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
            9: [('PASS_LINE', self.basePassLineBet),
                ('ODD_9', self.basePassLineBet * 4),
                ('PLACE_6', self.basePlaceBet),
                ('PLACE_8', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
            10: [('PASS_LINE', self.basePassLineBet),
                ('ODD_10', self.basePassLineBet * 3),
                ('PLACE_6', self.basePlaceBet),
                ('PLACE_8', self.basePlaceBet),
                ('HARD_6', self.baseHardwayBet),
                ('HARD_8', self.baseHardwayBet)],
        }

    def get_bets(self, betTable, point):
        newBets = {}
        for betName, betAmount in self.betsByPoint.get(point, []):
            if betTable.get(betName, 0) == 0:
                newBets[betName] = betAmount
        return newBets
    
    def reset(self):
        self.pass_line_winner_count = 0
        self.hardway_winner_count = 0
