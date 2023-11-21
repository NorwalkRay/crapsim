Project To Do List

# TODO: [flow] completely resolving a bet is paying it, and putting the original back. the strategy adds the bets back. this solves the case of how the strategy behaves when the point is hit (e.g. it doesn't have to check for odds bet not being removed after pt is hit)
# TODO: [refactor] extract payout multipliers from resolve_bets method. put in own config / class
# TODO: [feature] incorporate basic progression, increment place bet upon win.
# TODO: [testing] test suite with deterministic dice rolls. walk through various cases and test p&l and payout calculations
# TODO: [feature] dice roll distribution report
# TODO: [feature] value at risk per roll report, including theo generated
# TODO: [feature] i can define the payout structure for each type of bet in a config file
# TODO: [feature] bottom line output: "If you play X sessions/year with this strategy: you can expect to lose between X and Y dollars (25th - 75th) per year


Completed
# DONE: [refactor] Deprecated bet_table, made it a dictionary in CrapsSession class
# DONE: [flow] cleaned up run_game flow to be loop of place bets, roll, resolve bets
# TODO: [flow] update resolve_bets method to iterate through bets instead of going through logic of roll-types
# TODO: [bug-fix] modify bet removing method to collect keys to remove, and remove after iteration through all bets