class BetTable:
    
    def __init__(self):
        self.table = {}
        
    def add_bet(self, bet_name, bet_amount):
        self.table[bet_name] = bet_amount
        
    def remove_bet(self, bet_name):
        if bet_name in self.table:
            del self.table[bet_name]

    def get_bet_amount(self, bet_name):
        return self.table.get(bet_name, 0)

    def update_bet(self, bet_name, new_amount):
        if bet_name in self.table:
            self.table[bet_name] = new_amount

    def get_total_bet(self):
        return sum(self.table.values())

    def clear_bets(self):
        self.table.clear()

    def __str__(self):
        return ', '.join(f"{bet_name}: ${bet_amount}" for bet_name, bet_amount in self.table.items())

    def __repr__(self):
        return self.__str__()