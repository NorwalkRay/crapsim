from abc import ABC, abstractmethod

# Abstract class that represents methods all strategies should have.
class Strategy(ABC):
    
    @abstractmethod
    def place_initial_bets(self, bet_table, running_bankroll):
        pass
    
    @abstractmethod
    def place_post_point_bets(self, bet_table, running_bankroll, point):
        pass
    
    # @abstractmethod
    # def update_bets_after_roll(self, bet_table, die1, die2, roll_history):
    #     pass

# This is the instance of the specific strategy we're testing. All the strategy logic belongs in here
class Hedge6_Strategy(Strategy):
    
    def __init__(self): pass
        # self.hardway_counter = 0

    def place_initial_bets(self, bet_table, running_bankroll):
        bet_amount = 25 # defined
        if running_bankroll['amount'] < bet_amount: return False # not enough funds to place initial come out roll bet.
        else: 
            bet_table.add_bet('Pass Line', bet_amount)
            running_bankroll['amount'] -= bet_amount # remove bet from bankroll after adding it to the table.
            return True # successfully places initial pass line bet
        
    def place_post_point_bets(self, bet_table, running_bankroll, point):
        # TODO: [fix] handle >0, but not enough for full bet bankroll.
        
        place_bet_amount = 60 # defined
        hardway_bet_amount = 50 # defined

        if point == 4:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 3) + place_bet_amount + hardway_bet_amount
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True 
        elif point == 5:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 4) + place_bet_amount + hardway_bet_amount
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True
        elif point == 6:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 5) + place_bet_amount + (2 * hardway_bet_amount)
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                bet_table.add_bet('Hard 8', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True
        elif point == 8:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 5) + place_bet_amount + (2 * hardway_bet_amount)
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                bet_table.add_bet('Hard 8', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True
        elif point == 9:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 4) + place_bet_amount + hardway_bet_amount
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True
        elif point == 10:
            total_bet = (bet_table.get_bet_amount('Pass Line') * 3) + place_bet_amount + hardway_bet_amount
            if running_bankroll['amount'] < total_bet: return False # not enough funds
            else:
                bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
                bet_table.add_bet('Place 6', place_bet_amount)
                bet_table.add_bet('Hard 6', hardway_bet_amount)
                running_bankroll['amount'] -= total_bet
                return True
        else:
            # This should not happen as craps only has points 4, 5, 6, 8, 9, and 10
            raise ValueError("Invalid point value")

    # def update_bets_after_roll(self, bet_table, die1, die2, roll_history):
    #     # no updates to bets after rolls in this strategy
    #     pass