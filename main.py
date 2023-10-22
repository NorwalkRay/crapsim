
import numpy as np
import matplotlib.pyplot as plt
from strategy import Hedge6_Strategy
from simulation import run_sim
from utilities import roll_dice

if __name__ == '__main__':

    # Key Simulation Inputs: Strategy
    # To calculate P&L, I need bettable and a payouttable

    strategy = Hedge6_Strategy()
    pnl_by_roll, pnl_by_session, pnl_by_trip = run_sim(strategy)

    # Generate Metrics and Charts --- move this elsewhere eventually.
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