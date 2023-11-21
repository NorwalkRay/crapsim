from config import SESSION_BANKROLL, ROLLS_PER_HOUR, HRS_PER_SESSION
from craps_session import CrapsSession
from utilities import roll_dice

def run_sim(strategy, numSessions):
    pnlByRoll = []
    pnlByGame = []
    pnlBySession = []

    for sessionNum in range(numSessions):                                   # Outer loop to run multiple sessions
        mySession = CrapsSession(SESSION_BANKROLL, strategy)                # Initialize a new session each time
        rollsInSession = ROLLS_PER_HOUR * HRS_PER_SESSION 
        
        while len(mySession.rollHistory) < rollsInSession:
            mySession.run_game()
            if mySession.runningBankroll['amount'] <= 0:
                print(f"Session {sessionNum + 1}: Bankroll depleted. Ending session.")
                break
            
            # After a session ends, check the number of rolls
            print(f"Session {sessionNum + 1} ended with {len(mySession.rollHistory)} rolls.")
            pnlBySession.append(sum(mySession.pnlByRoll))  # Sum the PnL for the session

        # After all sessions, verify the length of pnlByRoll
    
    print(f"Total number of rolls across all sessions: {len(pnlByRoll)}")
    
    return pnlByRoll, pnlByGame, pnlBySession

'''
        while len(mySession.rollHistory) < rollsInSession:                  # Inner loop to run each session
            pnlStart = sum(mySession.pnlByRoll)
            mySession.run_game()                                            # Run a game, which may consist of 1 or more rolls
            pnlEnd = sum(mySession.pnlByRoll)
            pnlByGame.append(pnlEnd - pnlStart)
            if mySession.runningBankroll['amount'] <= 0:                    #  to do: Handle case with low but not zero bankroll
                print(f"Session {sessionNum + 1}: Bankroll depleted. Ending session.")
                break
            pnlByRoll.extend(mySession.pnlByRoll)                               # Extend the list to include PnL of all rolls in this session
            pnlBySession.append(sum(mySession.pnlByRoll))                       # Add up the PnL for the entire session
'''