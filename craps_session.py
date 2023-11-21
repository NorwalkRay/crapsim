from utilities import roll_dice

class CrapsSession:
    def __init__(self, sessionMaxBankroll, strategy):
        self.gameCounter = 0
        self.rollHistory = [] # 2 x n array of all rolls, including the come out roll(s). Each column represents 1 die, accumulates over whole session
        self.runningBankroll = {'amount': sessionMaxBankroll} # cumulative running bankroll over the whole session
        self.point = None # the number of the point. none prior to establishment.
        self.betTable = {} # represents all bets on the table
        self.strategy = strategy # betting strategy to use
        self.pnlByRoll = [] # net p&l after each roll, accumulates over whole session

    '''
    Get list of new bets to place from the strategy. If total bet amount is less than bankroll, place the bet and decrement the bankroll.
    Otherwise, output error and set bankroll to zero.

    INPUT: point
    RETURNS: none
    '''
    def place_bets(self, point):
        newBets = self.strategy.get_bets(self.betTable, point)
        totalNewBetAmount = sum(newBets.values())
        
        if self.runningBankroll['amount'] >= totalNewBetAmount:
            for bet_name, bet_amount in newBets.items():
                self.betTable[bet_name] = bet_amount
                self.runningBankroll['amount'] -= bet_amount
        else:
            print("Insufficient funds to place all bets. Ending session.")
            self.runningBankroll['amount'] = 0

    '''
    (1) roll the dice, (2) add roll to history, (3) return die numbers.

    INPUT: none
    RETURNS: die1, die2
    '''
    def execute_roll(self):
        die1, die2 = roll_dice()
        rollSum = die1 + die2
        self.rollHistory.append((die1, die2))
        return die1, die2
    
    def resolve_single_bet(self, betName, rollSum, die1, die2):
        payoutMultipliers = {
            'PASS_LINE': 1,
            'ODDS': {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2},
            'PLACE_6': 7.0 / 6.0,
            'PLACE_8': 7.0 / 6.0,
            'HARD_6': 9,
            'HARD_8': 9,
            # ... add other bets here
        }
        betPnl = 0

        def apply_payout(multiplier):
            nonlocal betPnl
            betPnl = self.betTable.get(betName, 0) * multiplier         # payout is the bet amount times multiplier
            self.runningBankroll['amount'] += betPnl                    # add payout to bankroll

        def apply_loss():
            nonlocal betPnl
            betPnl = -self.betTable.get(betName, 0)                      # set the bet pnl to the loss amount
            self.betTable.pop(betName, None)
        
        if betName == 'PASS_LINE':
            if self.point is None and rollSum in [7, 11]:  # come out roll winner
                apply_payout(payoutMultipliers['PASS_LINE'])
            elif self.point is None and rollSum in [2, 3, 12]:
                apply_loss()
            elif self.point == rollSum:
                apply_payout(payoutMultipliers['PASS_LINE'])
            elif self.point is not None and rollSum == 7:
                apply_loss()

        elif betName == 'ODDS':
            if rollSum == self.point:
                apply_payout(payoutMultipliers['ODDS'].get(rollSum, 0))
            elif rollSum == 7:
                apply_loss()

        elif betName in ['PLACE_6', 'PLACE_8']:
            if rollSum == int(betName.split('_')[1]):
                apply_payout(payoutMultipliers[betName])
            elif rollSum == 7:
                apply_loss()

        elif betName in ['HARD_6', 'HARD_8']:
            if rollSum == int(betName.split('_')[1]) and die1 == die2:
                apply_payout(payoutMultipliers[betName])
            else:
                apply_loss()
            if self.point is not None and rollSum == 7:
                apply_loss()
        print(f"Bet: {betName}, Roll Sum: {rollSum}, P&L for this bet: {betPnl}, Point is: {self.point}")
        return betPnl

    def resolve_bets(self, die1, die2):
        rollSum = die1 + die2
        rollPnl = 0
        betsToRemove = []  # List to keep track of losing bets

        # First, calculate payouts and losses, but don't modify the betTable yet
        for betName in list(self.betTable.keys()):  # Use list to make a copy of keys
            singlePnl = self.resolve_single_bet(betName, rollSum, die1, die2)
            rollPnl += singlePnl
            if singlePnl < 0:  # If pnl for a bet is negative, it means the bet lost
                betsToRemove.append(betName)  # Add bet name to the list of bets to remove

        # Now, remove the losing bets from betTable
        for betName in betsToRemove:
            self.betTable.pop(betName, None)
        print(f"Total P&L for this roll: {rollPnl}")
        return rollPnl
    
    def run_game(self):
        self.gameCounter += 1
        gameOngoing = True
        pointEstablished = False  # Track if the point is established

        while gameOngoing:
            self.place_bets(self.point)
            die1, die2 = self.execute_roll()
            rollSum = die1 + die2

            if not pointEstablished:
                # Check for come-out roll winners or losers
                if rollSum in [7, 11]:  # Winner on come-out roll
                    gameOngoing = False
                elif rollSum in [2, 3, 12]:  # Loser on come-out roll
                    gameOngoing = False
                else:
                    # If the roll is 4, 5, 6, 8, 9, or 10, establish the point
                    self.point = rollSum
                    pointEstablished = True  # Mark the point as established
            else:
                # Game continues until the point is hit or a 7 is rolled
                if rollSum == 7:  # Seven out
                    gameOngoing = False
                elif rollSum == self.point:  # Hit the point
                    gameOngoing = False

            # Resolve bets for this roll and record PnL
            rollPnl = self.resolve_bets(die1, die2)
            self.pnlByRoll.append(rollPnl)

            # Reset the point if the game has ended
            if not gameOngoing:
                self.point = None
                pointEstablished = False
'''
    def run_game(self):
        self.gameCounter += 1
        gameOngoing = True
        while gameOngoing:
            self.place_bets(self.point)
            die1, die2 = self.execute_roll()
            rollSum = die1 + die2
            rollPnl = self.resolve_bets(die1, die2)
            self.pnlByRoll.append(rollPnl)                  # Record PNL for the roll
            # Check for game-ending conditions
            if self.point is None and rollSum in [2, 3, 7, 11, 12]:
                gameOngoing = False
            elif self.point is not None and rollSum == 7:
                gameOngoing = False
            elif self.point == rollSum:
                gameOngoing = False
            
            # If the point is hit or a seven is rolled, reset the point
            if not gameOngoing:
                self.point = None
'''