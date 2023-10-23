from config import TRIPS_PER_SIM, TRIP_BANKROLL, SESSIONS_PER_TRIP, SESSION_BANKROLL, ROLLS_PER_HOUR, HRS_PER_SESSION
from craps_session import CrapsSession
from bet_table import BetTable
from utilities import roll_dice

def run_sim(strategy, num_sessions):
    pnl_by_roll = []
    pnl_by_game = []
    pnl_by_session = []

    for session_num in range(num_sessions):  # Outer loop to run multiple sessions
        my_session = CrapsSession(SESSION_BANKROLL, strategy)  # Initialize a new session each time
        rolls_in_session = ROLLS_PER_HOUR * HRS_PER_SESSION 
        
        while len(my_session.roll_history) < rolls_in_session:  # Inner loop to run each session
            pnl_starting = sum(my_session.pnl_by_roll)
            my_session.run_game()  # Run a game, which may consist of 1 or more rolls
            pnl_ending = sum(my_session.pnl_by_roll)
            pnl_by_game.append(pnl_ending - pnl_starting)
            if my_session.running_bankroll['amount'] <= 0:  #  to do: Handle case with low but not zero bankroll
                print(f"Session {session_num + 1}: Bankroll depleted. Ending session.")
                break

        pnl_by_roll.extend(my_session.pnl_by_roll)  # Extend the list to include PnL of all rolls in this session
        pnl_by_session.append(sum(my_session.pnl_by_roll))  # Add up the PnL for the entire session

    return pnl_by_roll, pnl_by_game, pnl_by_session