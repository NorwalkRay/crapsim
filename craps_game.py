from bet_table import BetTable
from utilities import roll_dice

class CrapsGame:
    def __init__(self, initial_bankroll, strategy):
        self.game_start_bankroll = initial_bankroll
        self.bankroll = initial_bankroll # carries over within a session
        self.strategy = strategy # betting strategy to use
        self.bet_table = BetTable() # represents all bets on the table
        self.point = None # the number of the point. none prior to establishment.
        self.roll_history = [] # 2 x n array of all rolls, including the come out roll(s). Each column represents 1 die.
        self.pnl_by_roll = [] # net p&l after each roll

    def place_initial_bets(self):
        self.strategy.place_initial_bets(self.bet_table) # updates the bet table with the initial bets of the strat
        self.bankroll -= self.bet_table.get_total_bet() # when a bet is placed, remove it from the bankroll
    
    def place_post_point_bets(self):
        amount_to_bet = self.strategy.place_post_point_bets(self.bet_table, self.point)
        self.bankroll -= amount_to_bet

    def update_bets_after_roll(self, die1, die2):
        self.strategy.update_bets_after_roll(self.bet_table, die1, die2, self.roll_history)
 
    def run_game(self):
        print(f"Starting bankroll for this game: {self.bankroll}")
        self.place_initial_bets()
        #print("After placing initial bets:")  # Diagnostic
        #print(self.bet_table)  # Diagnostic
        die1, die2 = roll_dice()
        roll_sum = die1 + die2
        self.roll_history.append((die1, die2))
        if roll_sum in [7, 11]:
            self.bankroll += self.bet_table.get_bet_amount('Pass Line') # the winnings are put into the bankroll. the original bet is not put back in bankroll, but stays on bet table
            self.pnl_by_roll.append(self.bet_table.get_bet_amount('Pass Line'))
        elif roll_sum in [2, 3, 12]:
            self.pnl_by_roll.append(-self.bet_table.get_bet_amount('Pass Line'))
            self.bet_table.remove_bet('Pass Line')  # Remove pass line bet, loss is already accounted for by subtracting initial bet from bankroll.
        else:
            self.pnl_by_roll.append(0)
            self.point = roll_sum
            self.place_post_point_bets()
            while self.point:
                die1, die2 = roll_dice()
                self.roll_history.append((die1, die2))
                roll_sum = die1 + die2
                if roll_sum in [2,3,11,12]: # No Changes
                    self.pnl_by_roll.append(0)
                elif roll_sum == 7: # gotta pay don'ts
                    self.pnl_by_roll.append(-self.bet_table.get_total_bet())
                    self.bet_table.clear_bets()
                    self.point = None  # Reset point
                elif roll_sum == self.point:
                    self.pnl_by_roll.append(self.bet_table.get_bet_amount('Pass Line'))
                    self.bankroll += self.bet_table.get_bet_amount('Pass Line')
                    if roll_sum in [4,10]:
                        self.bankroll += self.bet_table.get_bet_amount('Odds') * 2 # odds pay 2:1
                        self.bankroll += self.bet_table.get_bet_amount('Odds') # return odds
                        self.pnl_by_roll.append(self.bet_table.get_bet_amount('Odds') * 2) # p&l is only profit. not original odds bet
                        self.bet_table.remove_bet('Odds')
                        # To Add: Hardway check
                    elif roll_sum in [5,9]:
                        self.bankroll += self.bet_table.get_bet_amount('Odds') * 1.5 # odds pay 3:2
                        self.bankroll += self.bet_table.get_bet_amount('Odds') # return odds
                        self.pnl_by_roll.append(self.bet_table.get_bet_amount('Odds') * 1.5)
                        self.bet_table.remove_bet('Odds')
                    elif roll_sum == 6: 
                        self.bankroll += self.bet_table.get_bet_amount('Odds') * 1.2 # odds pay 6:5
                        self.bankroll += self.bet_table.get_bet_amount('Odds') # return odds
                        self.bet_table.remove_bet('Odds')
                        if die1 == die2: # hardway
                            self.bankroll += self.bet_table.get_bet_amount('Hard 6') * 9
                            self.pnl_by_roll.append((self.bet_table.get_bet_amount('Odds') * 1.2)+(self.bet_table.get_bet_amount('Hard 6') * 9))   
                        else: # easy 6
                            self.bankroll -= self.bet_table.get_bet_amount('Hard 6') # back up on hard 6
                            self.pnl_by_roll.append((self.bet_table.get_bet_amount('Odds') * 1.2)-(self.bet_table.get_bet_amount('Hard 6')))
                    elif roll_sum == 8:
                        self.bankroll += self.bet_table.get_bet_amount('Odds') * 1.2 # odds pay 6:5
                        self.bankroll += self.bet_table.get_bet_amount('Odds') # return odds
                        self.bet_table.remove_bet('Odds')
                        if die1 == die2: # hardway
                            self.bankroll += self.bet_table.get_bet_amount('Hard 8') * 9   
                            self.pnl_by_roll.append((self.bet_table.get_bet_amount('Odds') * 1.2)+(self.bet_table.get_bet_amount('Hard 8') * 9)) 
                        else: # easy 8
                            self.bankroll -= self.bet_table.get_bet_amount('Hard 8') # back up on hard 8
                            self.pnl_by_roll.append((self.bet_table.get_bet_amount('Odds') * 1.2)-(self.bet_table.get_bet_amount('Hard 8')))
                    else:
                        raise ValueError(f"Unhandled roll_sum: {roll_sum}")
                    self.point = None     
                elif roll_sum in [4,5,9,10]: # No Changes (not the point)
                    self.pnl_by_roll.append(0)
                elif roll_sum == 6:
                    self.bankroll += self.bet_table.get_bet_amount('Place 6') * 7.0 / 6.0
                    if die1 == die2: # hardway
                        self.bankroll += self.bet_table.get_bet_amount('Hard 6') * 9
                        self.pnl_by_roll.append((self.bet_table.get_bet_amount('Place 6') * 7.0 / 6.0)+(self.bet_table.get_bet_amount('Hard 6') * 9))
                    else: # easy way
                        self.bankroll -= self.bet_table.get_bet_amount('Hard 6') # back up on the hard 6
                        self.pnl_by_roll.append((self.bet_table.get_bet_amount('Place 6') * 7.0 / 6.0)-(self.bet_table.get_bet_amount('Hard 6')))
                elif roll_sum == 8:
                    self.bankroll += self.bet_table.get_bet_amount('Place 8') * 7.0 / 6.0
                    if die1 == die2: # hardway
                        self.bankroll += self.bet_table.get_bet_amount('Hard 8') * 9
                        self.pnl_by_roll.append((self.bet_table.get_bet_amount('Place 6') * 7.0 / 6.0)+(self.bet_table.get_bet_amount('Hard 8') * 9))
                    else: # easy way
                        self.bankroll -= self.bet_table.get_bet_amount('Hard 8') # back up on the hard 8
                        self.pnl_by_roll.append((self.bet_table.get_bet_amount('Place 6') * 7.0 / 6.0)-(self.bet_table.get_bet_amount('Hard 8')))
                else:
                    raise ValueError(f"Unhandled roll_sum: {roll_sum}")
                self.update_bets_after_roll(die1, die2)                    
        print(f"Ending bankroll for this game: {self.bankroll}")
        print(f"Bets remaining on felt for this game: {self.bet_table.get_total_bet()}")
        game_pnl = sum(self.pnl_by_roll)
        expected_pnl = (self.bankroll + self.bet_table.get_total_bet()) - self.game_start_bankroll
        
        print(f"Calculated P&L for this game: {game_pnl}")

        # Verify that the calculated P&L matches with the expected P&L
        if game_pnl == expected_pnl:
            print("P&L calculation is consistent.")
        else:
            print(f"Something is off. Expected P&L: {expected_pnl}, but got {game_pnl}")
