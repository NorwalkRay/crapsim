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

    def place_bets(self, bet_table, point):
        new_bets = self.strategy.get_bets(bet_table, point)
        total_new_bet_amount = sum(bet_amount for _, bet_amount in new_bets)
        
        if self.running_bankroll['amount'] >= total_new_bet_amount:
            for bet_name, bet_amount in new_bets:
                bet_table.add_bet(bet_name, bet_amount)
                self.running_bankroll['amount'] -= bet_amount
        else:
            print("Insufficient funds to place all bets. Ending session.")
            self.running_bankroll['amount'] = 0

    '''
    (1) roll the dice, (2) add roll to history, (3) return die numbers.
    '''
    def execute_roll(self):
        die1, die2 = roll_dice()
        roll_sum = die1 + die2
        self.roll_history.append((die1, die2))
        return die1, die2

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
    
    def run_game(self):
        game_ongoing = True
        while game_ongoing:
            self.place_bets(self.bet_table, self.point)
            die1, die2 = self.execute_roll()
            roll_sum = die1 + die2
            self.pay_winners(die1, die2)
            # remove losers
            if ((self.point is None and (roll_sum) in [2,3,7,11,12]) or # come out roll winner or lose ends game
                (self.point is not None and (roll_sum) == 7) or # point established, seven out ends game
                (self.point == roll_sum)): # or winner
                self.point = None ## TODO: Move this elsewhere
                game_ongoing = False
            
        ###print(f"Starting Bankroll for the Game: {self.running_bankroll['amount']}")
        self.game_counter += 1
        #print(f"Start of Game #{self.game_counter}, roll number {len(self.roll_history) + 1} of session. {self.running_bankroll['amount']} on rack | {self.bet_table.get_total_bet()} on table | Session pnl ${sum(self.pnl_by_roll)}")
        #self.running_bankroll['amount'] += self.bet_table.get_total_bet()
        # self.bet_table.clear_bets()
        ###print(f"Ending Bankroll for the Game: {self.running_bankroll['amount']}")        
        ###print(f"Bets remaining on felt for this game: {self.bet_table.get_total_bet()}")
        #print(f"Roll History: {self.roll_history}")

    # This method walks through every bet. It adjusts the pnl, moves money in and out of bankroll, and adjusts the bet table. to do: break out this monster function
    def pay_winners(self, die1, die2):
        payout_multipliers = {
        'PASS_LINE': 1,
        'ODDS': {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2},
        'PLACE_6': 7.0 / 6.0,
        'PLACE_8': 7.0 / 6.0,
        'HARD_6': 9,
        'HARD_8': 9,
        # ... add other bets here
        }
        roll_sum = die1 + die2
        pnl = 0  # Initialize Profit and Loss to 0

        def apply_payout(bet_name, multiplier):
            nonlocal pnl
            payout = self.bet_table.get_bet_amount(bet_name) * multiplier
            pnl += payout
            self.running_bankroll['amount'] += payout
            
        if self.point is None:  # come out roll
            if roll_sum in [7, 11]:  # winner on come out roll
                apply_payout('PASS_LINE', payout_multipliers['PASS_LINE'])

            elif roll_sum in [2, 3, 12]:  # loser on come out roll
                pnl -= self.bet_table.get_bet_amount('PASS_LINE')

            else:  # point is established
                for bet_name in self.bet_table.table.keys():
                    if roll_sum == 7:  # seven out
                        pnl -= self.bet_table.get_bet_amount(bet_name)
            
                    elif roll_sum == self.point:  # hit the point
                        if bet_name in ['PASS_LINE', 'ODDS']:
                            apply_payout(bet_name, payout_multipliers.get(bet_name, {}).get(roll_sum, 0))
            
                    elif roll_sum in [6, 8]:  # 6 or 8 rolled, but not the point
                        if bet_name == f'PLACE_{roll_sum}':
                            apply_payout(bet_name, payout_multipliers.get(bet_name, 0))

                        if die1 == die2 and bet_name == f'HARD_{roll_sum}':
                            apply_payout(bet_name, payout_multipliers.get(bet_name, 0))
                        elif bet_name == f'HARD_{roll_sum}':
                            pnl -= self.bet_table.get_bet_amount(bet_name)
                            self.running_bankroll['amount'] -= self.bet_table.get_bet_amount(bet_name)

        return pnl













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
                    ###print(f"rolled a 6: {payout}")
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
        ###print((die1, die2, pnl))
        return pnl  # Returning pnl


            
# TODO: [feature] incorporate basic progression, increment place bet upon win.
# TODO: [flow] clean up run_game flow. improve bankroll check, allow simpler body of method, call other methods.
# TODO: [testing] test suite with deterministic dice rolls. walk through various cases and test p&l and payout calculations