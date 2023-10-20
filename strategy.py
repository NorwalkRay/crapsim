from abc import ABC, abstractmethod

# Abstract class that represents methods all strategies should have.
class Strategy(ABC):
    
    @abstractmethod
    def initial_bets(self, bet_table):
        pass
    
    @abstractmethod
    def point_set_bets(self, bet_table, point):
        pass
    
    @abstractmethod
    def adjust_for_roll(self, bet_table, roll_result):
        pass

    # This is the instance of the specific strategy we're testing. All the strategy logic belongs in here
class Hedge6_Strategy(Strategy):
    
    def initial_bets(self, bet_table):
        bet_table.add_bet('Pass Line', 25)
        
    def point_set_bets(self, bet_table, point):
        if point == 4:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
        elif point == 5:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
        elif point == 6:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
            bet_table.add_bet('Place 8', 60)
            bet_table.add_bet('Hard 8', 50)
        elif point == 8:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 5)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
        elif point == 9:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 4)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
        elif point == 10:
            bet_table.add_bet('Odds', bet_table.get_bet_amount('Pass Line') * 3)
            bet_table.add_bet('Place 6', 60)
            bet_table.add_bet('Hard 6', 50)
        else:
            # This should not happen as craps only has points 4, 5, 6, 8, 9, and 10
            raise ValueError("Invalid point value")

    def adjust_for_roll(self, bet_table, die1, die2, roll_history):
        roll_sum = die1 + die2
        if roll_sum == 7:
            pass
        #more cases
        last_roll = roll_history[-1]
        if sum(last_roll) == 7:  # Replace with your own win condition logic
            # Progression logic, such as doubling the bet
            pass_line_bet = bet_table.get_bet_amount('Pass Line')
            new_pass_line_bet = pass_line_bet * 2  # Example: double
            bet_table.add_bet('Pass Line', new_pass_line_bet)
        else:
            # Reset to base bet
            bet_table.add_bet('Pass Line', 25)