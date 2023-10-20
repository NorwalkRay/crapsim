from config import TRIPS_PER_SIM, TRIP_BANKROLL, SESSIONS_PER_TRIP, SESSION_BANKROLL, ROLLS_PER_HOUR, HRS_PER_SESSION
from craps_game import CrapsGame
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
    my_game = CrapsGame(initial_bankroll=starting_bankroll, strategy=strategy)
    my_game.run_game()
    pnl_by_roll.append(my_game.pnl_by_roll[-1])  # Assuming you are keeping track of pnl_by_roll in the class
    return my_game.bankroll

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