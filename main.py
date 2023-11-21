import numpy as np
import matplotlib.pyplot as plt
from strategy import Hedge68_Strategy
from simulation import run_sim
from utilities import roll_dice

if __name__ == '__main__':

    strategy = Hedge68_Strategy()
    pnlByRoll, pnlByGame, pnlBySession = run_sim(strategy, numSessions = 5)

    # Generate Metrics and Charts --- move this elsewhere eventually.
    avgPnlPerRoll = np.mean(pnlByRoll)
    avgPnlPerGame = np.mean(pnlByGame)
    avgPnlPerSession = np.mean(pnlBySession)

    print(f"Average P&L Per Roll: {avgPnlPerRoll}")
    print(f"Average P&L Per Game: {avgPnlPerGame}")
    print(f"Average P&L Per Session: {avgPnlPerSession}")

    plt.figure()
    plt.hist(pnlByRoll, bins=50)
    plt.title("Distribution of Roll P&L")
    plt.show(block=True)

    plt.figure()
    plt.hist(pnlByGame, bins=50)
    plt.title("Distribution of Game P&L")
    plt.show(block=True)

    plt.figure()
    plt.hist(pnlBySession, bins=50)
    plt.title("Distribution of Session P&L")
    plt.show(block=True)