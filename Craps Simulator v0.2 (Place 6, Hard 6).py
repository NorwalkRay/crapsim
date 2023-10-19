import random
import numpy as np
import matplotlib.pyplot as plt
import csv
from random import randint
from collections import Counter
from collections import defaultdict
from abc import ABC, abstractmethod

# Global variables
ROLLS_PER_HOUR = 60 # constant, crowded table
HRS_PER_SESSION = 3 # Assumed hours per session
SESSIONS_PER_TRIP = 6 # Number of sessions to simulate
TRIPS_PER_SIM = 20 # Core unit of a simulation is a trip
TRIP_BANKROLL = 20000 # Bankroll for each trip 
SESSION_BANKROLL = 4000 # Bankroll for each session


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

    def adjust_for_roll(self, bet_table, roll_result):
        # Your logic here
        pass

class BetTable:
    def __init__(self):
        self.table = []
        
    def add_bet(self, bet_name, bet_amount):
        self.table.append({
            'bet_name': bet_name,
            'bet_amount': bet_amount
        })
        
    def remove_bet(self, bet_name):
        self.table = [bet for bet in self.table if bet['bet_name'] != bet_name]

    def get_bet_amount(self, bet_name):
        for bet in self.table:
            if bet['bet_name'] == bet_name:
                return bet['bet_amount']
        return 0  # Return 0 if the bet_name is not found

def roll_dice():
    die1 = randint(1, 6)
    die2 = randint(1, 6)
    return die1, die2

def run_game(bankroll, strategy, pnl_by_roll):
    # Initialize
    bet_table = BetTable()
    point = None
    strategy.initial_bets(strategy, bet_table)

    # Come Out Roll
    die1, die2 = roll_dice()
    roll_sum = die1 + die2
    if roll_sum in [7, 11]:
        return bankroll + bet_table.get_bet_amount('Pass Line')
    elif roll_sum in [2, 3, 12]:
        # You lose immediately
        # Adjust bankroll and bet table
        pass
    else:
        point = roll_sum
        strategy.point_set_bets(bet_table, point)

    # Loop to hit the point or seven out
    while point:
        die1, die2 = roll_dice()
        strategy.adjust_for_roll(bet_table, die1, die2)
        # Logic to determine if point is hit or seven out
        # Adjust bankroll and bet table accordingly
        # Break loop if point is hit or seven out

    roll_pl = bankroll - TRIP_BANKROLL
    pnl_by_roll.append(roll_pl)
    
    return bankroll  # Return updated bankroll after one game

def run_session(strategy, pnl_by_session, pnl_by_roll):
    bankroll = TRIP_BANKROLL
    rolls_in_session = ROLLS_PER_HOUR * HOURS_PER_SESSION

    for _ in range(rolls_in_session):
        bankroll = run_game(bankroll, strategy)
        if bankroll <= 0:
            break  # End session if bankroll hits zero

    session_pl = bankroll - TRIP_BANKROLL
    pnl_by_session.append(session_pl)
    
    return bankroll  # Return updated bankroll after one session

def run_trip(strategy, pnl_by_trip, pnl_by_session, pnl_by_roll):
    bankroll = TRIP_BANKROLL

    for _ in range(SESSIONS_PER_TRIP):
        bankroll = run_session(bankroll, strategy)
        if bankroll <= 0:
            break # End session if bankroll hits zero
    
    trip_pl = bankroll - TRIP_BANKROLL
    pnl_by_trip.append(trip_pl)
    
    return bankroll  # Return updated bankroll after one trip

def run_sim(strategy):
    pnl_by_roll = []
    pnl_by_session = []
    pnl_by_trip = []
    trip_bankroll = TRIP_BANKROLL

    for _ in range(TRIPS_PER_SIM):
        trip_bankroll = run_trip(strategy, pnl_by_trip, pnl_by_session, pnl_by_roll)
        # Check bankroll, break if needed

    return pnl_by_roll, pnl_by_session, pnl_by_trip

if __name__ == '__main__':
    strategy = Hedge6_Strategy()
    pnl_by_roll, pnl_by_session, pnl_by_trip = run_sim(strategy)

    # Generate Metrics and Charts
    avg_pl_per_roll = np.mean(pnl_by_roll)
    avg_pl_per_session = np.mean(pnl_by_session)
    avg_pl_per_trip = np.mean(pnl_by_trip)

    print(f"Average P&L Per Roll: {avg_pl_per_roll}")
    print(f"Average P&L Per Session: {avg_pl_per_session}")
    print(f"Average P&L Per Trip: {avg_pl_per_trip}")

    plt.figure()
    plt.hist(pnl_by_session, bins=20)
    plt.title("Distribution of Session P&L")
    plt.show()

    plt.figure()
    plt.hist(pnl_by_trip, bins=20)
    plt.title("Distribution of Trip P&L")
    plt.show()



