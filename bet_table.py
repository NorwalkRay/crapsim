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
    
    def get_total_bet(self):
        return sum(bet['bet_amount'] for bet in self.table)

    def clear_bets(self):
        self.table = []

    def __str__(self):
        return ', '.join(f"{bet['bet_name']}: ${bet['bet_amount']}" for bet in self.table)

    def __repr__(self):
        return self.__str__()