from bet_table import BetTable
from utilities import roll_dice

class CrapsSession:
    def __init__(self, session_max_bankroll, strategy):
        self.game_counter = 0
        self.roll_history = [] # 2 x n array of all rolls, including the come out roll(s). Each column represents 1 die.
        self.running_bankroll = session_max_bankroll
        self.point = None # the number of the point. none prior to establishment.
        self.bet_table = BetTable() # represents all bets on the table
        #self.game_start_bankroll = initial_bankroll
        #self.bankroll = initial_bankroll # carries over within a session
        self.strategy = strategy # betting strategy to use
        self.pnl_by_roll = [] # net p&l after each roll

    def place_initial_bets(self):
        return self.strategy.place_initial_bets(self.bet_table, self.running_bankroll) # updates the bet table with the initial bets of the strat
    
    def place_post_point_bets(self):
        amount_to_bet = self.strategy.place_post_point_bets(self.bet_table, self.point)
        self.bankroll -= amount_to_bet

    def update_bets_after_roll(self, die1, die2):
        self.strategy.update_bets_after_roll(self.bet_table, die1, die2, self.roll_history)
 
    def run_game(self):
        self.game_counter += 1
        print(f"Start of Game #{self.game_counter}, roll number {len(self.roll_history) + 1} of session.
              {self.running_bankroll} on rack | {self.bet_table.get_total_bet()} on table | Session pnl ${sum(self.pnl_by_roll)}")
        if self.place_initial_bets() == False: 
            pass #exit game, out of money
        else:
            print(f"Game #{self.game_counter}: {self.running_bankroll} on rack | {self.bet_table.get_total_bet()} on table")
            self.administer_roll()
        
        roll_sum = die1 + die2
        
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

    # This method only makes the payouts. This means adding it to pnl. There will be a separate method for removing the bet from the bet table
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
        losing_bets = []  # List to keep track of losing bets

        for bet in self.bet_table.table:
            bet_name = bet['bet_name']
            bet_amount = bet['bet_amount']

            if bet_name == 'Pass Line':
                if self.point is None:
                    if roll_sum in [7, 11]:
                        pnl += bet_amount * payout_multipliers[bet_name]
                    elif roll_sum in [2, 3, 12]:
                        pass
                else:
                    if roll_sum == self.point:
                        pnl += bet_amount * payout_multipliers[bet_name]
                    elif roll_sum == 7:
                        pass

            elif bet_name == 'Odds':
                if self.point is not None:  # Check if the point is established
                    if roll_sum == self.point:
                        multiplier = payout_multipliers['Odds'].get(roll_sum, 0)
                        pnl += bet_amount * multiplier
                    elif roll_sum == 7:
                        pass
                # Else: Do nothing, the bet remains unresolved if no point is established

            elif bet_name in ['Place 6', 'Place 8']:
                if roll_sum == int(bet_name.split()[1]): # check the number of the place bet
                    pnl += bet_amount * payout_multipliers[bet_name]
                elif roll_sum == 7: pass

            elif bet_name in ['Hard 6', 'Hard 8']:
                target = int(bet_name.split()[1])  # Extract 6 or 8
                if roll_sum == target and die1 == die2:  # It must be 'Hard' meaning both dice have the same number
                    pnl += bet_amount * payout_multipliers[bet_name]
                elif roll_sum == 7 or (roll_sum == target and die1 != die2):
                    pass

            # Add other bet types with their own logic here
        return pnl, losing_bets  # Returning both pnl and losing_bets to handle them appropriately in the game state

    def update_bet_table(self, die1, die2):
        bet_name = bet['bet_name']
        bet_amount = bet['bet_amount']
        roll_sum = die1 + die2

        if self.point == None:
            if roll_sum in [7, 11]: pass # pass line winner, keep bet
            elif roll_sum in [2, 3, 12]: pass # to do: remove the pass line bet
            else: pass # point is established
        elif roll_sum == 7: pass # clear all the bets
        elif roll_sum in [6, 8] and die1 != die2: pass
            # remove the hardway on 6 or 8, depending on which was rolled
        else: pass # not the come out roll, not the seven, bets aren't removed (unless easy ways)

    def administer_roll(self):
        die1, die2 = roll_dice()
        self.roll_history.append((die1, die2))
        self.make_payouts(die1, die2)
        self.update_bet_table(die1, die2)
        