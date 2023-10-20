from config import TRIPS_PER_SIM, TRIP_BANKROLL, SESSIONS_PER_TRIP, SESSION_BANKROLL, ROLLS_PER_HOUR, HRS_PER_SESSION
from bet_table import BetTable
from utilities import roll_dice

def run_sim(strategy):
    pnl_by_roll = []
    pnl_by_session = []
    pnl_by_trip = []

    for _ in range(TRIPS_PER_SIM):
        run_trip(strategy, pnl_by_trip, pnl_by_session, pnl_by_roll)
        # Check bankroll, break if needed

    return pnl_by_roll, pnl_by_session, pnl_by_trip

def run_game(starting_bankroll, strategy, pnl_by_roll):
    
    # Initialize
    bankroll = starting_bankroll
    bet_table = BetTable()
    point = None
    roll_history = []
    strategy.initial_bets(bet_table)
    bankroll -= bet_table.get_total_bet()

    # Come Out Roll
    die1, die2 = roll_dice()
    roll_sum = die1 + die2
    roll_history.append((die1, die2)) # Update roll history
    if roll_sum in [7, 11]:
        return bankroll + bet_table.get_bet_amount('Pass Line') * 2 
    elif roll_sum in [2, 3, 12]:
        return bankroll
    else:
        point = roll_sum
        strategy.point_set_bets(bet_table, point)

    # Loop to hit the point or seven out
    while point:
        die1, die2 = roll_dice()
        roll_history.append((die1, die2)) # Update roll history
        roll_sum = die1 + die2
        
        if roll_sum == point: # Point is hit
            bankroll += bet_table.get_bet_amount('Pass Line')
            return bankroll
        elif roll_sum == 7:
            # Seven out
            bankroll -= bet_table.get_bet_amount('Pass Line')  # Assuming you have a bet for 'Point' in bet_table
            return bankroll
        
        strategy.adjust_for_roll(bet_table, die1, die2, roll_history)

    # Optional: Adjust bankroll for other bets that might have won or lost
    # bankroll += bet_table.some_other_bet_calculation()

    game_pnl = bankroll - starting_bankroll
    pnl_by_roll.append(game_pnl)
    
    return bankroll  # Return updated bankroll after one game

def run_session(strategy, pnl_by_session, pnl_by_roll):
    bankroll = SESSION_BANKROLL
    rolls_in_session = ROLLS_PER_HOUR * HRS_PER_SESSION

    for _ in range(rolls_in_session):
        bankroll = run_game(bankroll, strategy, pnl_by_roll)
        if bankroll <= 0:
            break  # End session if bankroll hits zero

    session_pnl = bankroll - SESSION_BANKROLL
    pnl_by_session.append(session_pnl)
    
    return bankroll  # Return updated bankroll after one session

def run_trip(strategy, pnl_by_trip, pnl_by_session, pnl_by_roll):
    bankroll = TRIP_BANKROLL

    for _ in range(SESSIONS_PER_TRIP):
        bankroll = run_session(strategy, pnl_by_session, pnl_by_roll)
        if bankroll <= 0:
            break # End session if bankroll hits zero
    
    trip_pnl = bankroll - TRIP_BANKROLL
    pnl_by_trip.append(trip_pnl)
    
    return bankroll  # Return updated bankroll after one trip