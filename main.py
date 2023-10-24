import numpy as np
import matplotlib.pyplot as plt
from strategy import Hedge68_Strategy
from simulation import run_sim
from utilities import roll_dice

if __name__ == '__main__':

    strategy = Hedge68_Strategy()
    pnl_by_roll, pnl_by_game, pnl_by_session = run_sim(strategy, num_sessions = 10000)

    # Generate Metrics and Charts --- move this elsewhere eventually.
    avg_pl_per_roll = np.mean(pnl_by_roll)
    avg_pl_per_game = np.mean(pnl_by_game)
    avg_pl_per_session = np.mean(pnl_by_session)

    print(f"Average P&L Per Roll: {avg_pl_per_roll}")
    print(f"Average P&L Per Game: {avg_pl_per_game}")
    print(f"Average P&L Per Session: {avg_pl_per_session}")

    plt.figure()
    plt.hist(pnl_by_roll, bins=50)
    plt.title("Distribution of Roll P&L")
    plt.show(block=True)

    plt.figure()
    plt.hist(pnl_by_game, bins=50)
    plt.title("Distribution of Game P&L")
    plt.show(block=True)

    plt.figure()
    plt.hist(pnl_by_session, bins=50)
    plt.title("Distribution of Session P&L")
    plt.show(block=True)