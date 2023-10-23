from bet_table import BetTable
from utilities import roll_dice

class CrapsSession:
    def __init__(self, session_max_bankroll, strategy):
        self.game_counter = 0
        self.roll_history = [] # 2 x n array of all rolls, including the come out roll(s). Each column represents 1 die, accumulates over whole session
        self.running_bankroll = {'amount': session_max_bankroll} # cumulative running bankroll over the whole session
        self.point = None # the number of the point. none prior to establishment.
        self.bet_table = BetTable() # represents all bets on the table
        self.strategy = strategy # betting strategy to use
        self.pnl_by_roll = [] # net p&l after each roll, accumulates over whole session

    def place_initial_bets(self):
        return self.strategy.place_initial_bets(self.bet_table, self.running_bankroll) # updates the bet table with the initial bets of the strat
    
    def place_post_point_bets(self):
        return self.strategy.place_post_point_bets(self.bet_table, self.running_bankroll, self.point)

    # def update_bets_after_roll(self, die1, die2):
    #     self.strategy.update_bets_after_roll(self.bet_table, die1, die2, self.roll_history)
 
    def run_game(self):
        self.game_counter += 1
        #print(f"Start of Game #{self.game_counter}, roll number {len(self.roll_history) + 1} of session. {self.running_bankroll['amount']} on rack | {self.bet_table.get_total_bet()} on table | Session pnl ${sum(self.pnl_by_roll)}")
        if self.place_initial_bets() == False: # not enough funds to place initial come out roll bet.
            print(f"Too low bankroll to place bets: {self.running_bankroll['amount']}, setting to 0")
            self.running_bankroll['amount'] = 0 # hack right now, to exit loop in simulator
        else: # initial come out bet(s) successfully placed
            if self.execute_next_roll() == False: # roll ends craps game
                pass #print(f"Game #{self.game_counter}: {self.running_bankroll['amount']} on rack | {self.bet_table.get_total_bet()} on table, ended on the come out")
            else: # the point has been established
                if self.place_post_point_bets() == False: # note enough funds to place post point bets
                    print(f"Too low bankroll to place bets: {self.running_bankroll['amount']}, setting to 0")
                    self.running_bankroll['amount'] = 0 # hack right now, to exit loop in simulator
                else: # successfully placed post point bets
                    game_ongoing = True
                    while game_ongoing:
                        game_ongoing = self.execute_next_roll()        
        #print(f"Ending bankroll for this game: {self.running_bankroll['amount']}")
        #print(f"Bets remaining on felt for this game: {self.bet_table.get_total_bet()}")

    # This method walks through every bet. It adjusts the pnl, moves money in and out of bankroll, and adjusts the bet table. to do: break out this monster function
    def make_payouts(self, die1, die2):
        payout_multipliers = {
            'Pass Line': 1,
            #'Don\'t Pass': 1,
            'Odds': {
                4: 2, 
                5: 1.5, 
                6: 1.2, 
                8: 1.2, 
                9: 1.5, 
                10: 2
            },
            'Place 6': 7.0 / 6.0,
            'Place 8': 7.0 / 6.0,
            'Hard 6': 9,
            'Hard 8': 9,
            # ... add other bets here
        }
        roll_sum = die1 + die2
        pnl = 0  # Initialize Profit and Loss to 0

        if self.point is None: # come out roll
            if roll_sum in [7, 11]: # come out winner
                payout = self.bet_table.get_bet_amount('Pass Line') * payout_multipliers['Pass Line'] # calculate pass line payout
                pnl += payout # pass line winnings added to pnl
                self.running_bankroll['amount'] += payout # pass line winnings added to bankroll
                self.running_bankroll['amount'] += self.bet_table.get_bet_amount('Pass Line') # original pass line bet returned to bankroll
                self.bet_table.remove_bet('Pass Line') # original pass line bet removed from table
            elif roll_sum in [2, 3, 12]: # come out loser
                pnl -= self.bet_table.get_bet_amount('Pass Line') # pass line bet loses
                self.bet_table.remove_bet('Pass Line') # remove losing bet from table
            else: pass # assuming all other bets are "off" on the come out
        else: # point is established
            if roll_sum in [2, 3, 11, 12]: pass # no payouts in current strategy
            elif roll_sum == 7: # seven out
                pnl -= self.bet_table.get_total_bet() # all bets lose and hit pnl
                self.bet_table.clear_bets() # clear all bets from the table
            else: # roll a number (4,5,6,8,9,10)
                if roll_sum == self.point: # hit the point
                    pl_win = self.bet_table.get_bet_amount('Pass Line') * payout_multipliers['Pass Line'] # calc pass line winnings
                    odds_win = self.bet_table.get_bet_amount('Odds') * payout_multipliers['Odds'].get(roll_sum, 0) # calc odds winnings
                    pnl += (pl_win + odds_win) # add pass line and odds winnings to pnl
                    self.running_bankroll['amount'] += (pl_win + odds_win) # add pass line and odds bet winnings to bankroll
                    self.running_bankroll['amount'] += self.bet_table.get_bet_amount('Odds') # return of odds bet after win
                    self.running_bankroll['amount'] += self.bet_table.get_bet_amount('Pass Line') # return of pass line bet after win
                    self.bet_table.remove_bet('Odds') # remove odds bet from table
                    self.bet_table.remove_bet('Pass Line') # remove pass line bet from table
                    if roll_sum == 6 and die1 != die2: # easy 6
                        pnl -= self.bet_table.get_bet_amount('Hard 6') # hard 6 loser
                        self.bet_table.remove_bet('Hard 6') # remove from table
                    elif roll_sum == 8 and die1 != die2: # easy 8
                        pnl -= self.bet_table.get_bet_amount('Hard 8') # hard 8 loser
                        self.bet_table.remove_bet('Hard 8') # remove from table
                    elif roll_sum in [6, 8] and die1 == die2: # hard 6 or 8 winner
                        payout = self.bet_table.get_bet_amount('Hard 6') * payout_multipliers['Hard 6'] # using hard 6, assuming hard 8 is always the same when point is 6 and 8
                        pnl += payout # add payout to pnl
                        self.running_bankroll['amount'] += payout # add payout to bankroll
                        self.running_bankroll['amount'] += self.bet_table.get_bet_amount('Hard 6') # return hard 6 original bet to bankroll
                        if roll_sum == 6: self.bet_table.remove_bet('Hard 6') # remove hard 6 bet
                        elif roll_sum == 8: self.bet_table.remove_bet('Hard 8') # remove hard 8 bet
                elif roll_sum in [5, 9]: pass # no payouts in current strategy
                elif roll_sum in [4, 10]: pass # no payouts in current strategy
                elif roll_sum == 6: # 6, but not the point
                    payout = self.bet_table.get_bet_amount('Place 6') * payout_multipliers['Place 6'] # calc place 6 winnings
                    pnl += payout # add payout to pnl
                    self.running_bankroll['amount'] += payout # add payout to bankroll
                    if die1 == die2: # hard 6
                        payout = self.bet_table.get_bet_amount('Hard 6') * payout_multipliers['Hard 6']
                        pnl += payout
                        self.running_bankroll['amount'] += payout
                    else: #hard 6 loser
                        pnl -= self.bet_table.get_bet_amount('Hard 6') # include lost bet in pnl
                        self.running_bankroll['amount'] -= self.bet_table.get_bet_amount('Hard 6') # subtract from bankroll to represent re-bet
                        # instead of removing the lost hardway and adding it back, we'll just leave it (and subtract from bankroll above)
                elif roll_sum == 8: # 8, but not the point
                    payout = self.bet_table.get_bet_amount('Place 8') * payout_multipliers['Place 8'] # calc place 8 winnings
                    pnl += payout # add payout to pnl
                    self.running_bankroll['amount'] += payout # add payout to bankroll
                    if die1 == die2: # hard 8
                        payout = self.bet_table.get_bet_amount('Hard 8') * payout_multipliers['Hard 8']
                        pnl += payout
                        self.running_bankroll['amount'] += payout
                    else: #hard 8 loser
                        pnl -= self.bet_table.get_bet_amount('Hard 8') # include lost bet in pnl
                        self.running_bankroll['amount'] -= self.bet_table.get_bet_amount('Hard 8') # subtract from bankroll to represent re-bet
                        # instead of removing the lost hardway and adding it back, we'll just leave it (and subtract from bankroll above)
                else:
                    print(f"something has gone wrong, should not reach here. diagnose")
        
        return pnl  # Returning pnl

    # rolls the dice, adds roll to history, calls payout calculator, adds pnl to pnl_by_roll, returns true unless roll results in end of game.
    def execute_next_roll(self):
        die1, die2 = roll_dice()
        roll_sum = die1 + die2
        self.roll_history.append((die1, die2))
        self.pnl_by_roll.append(self.make_payouts(die1, die2))
        if (self.point is None and (roll_sum) in [2,3,7,11,12]) or (self.point is not None and (roll_sum) == 7) or (self.point == roll_sum): # come out roll winner or lose ends game, point established, seven out ends game, or winner 
            self.point = None
            return False
        else: # the game continues
            if self.point is None: # if it was the come out roll
                self.point = roll_sum # then the point is now established
                return True
            else: # if it was not the come out
                return True
            
# TODO: [logging] game starting bankroll, game ending bankroll, $ left on felt, p&l
# TODO: [feature] incorporate basic progression, increment place bet upon win.
# TODO: [flow] clean up run_game flow. improve bankroll check, allow simpler body of method, call other methods.