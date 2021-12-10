class TokenPool:
    def __init__(self):
        self.tokens = 1000000000000

    def get_amount(self, amount: float):
        if (self.tokens - amount) > 0:
            self.tokens -= amount
            return amount
