from config import SIMULATED_CAPITAL

available_balance = SIMULATED_CAPITAL  # رأس المال الابتدائي

def update_balance(amount):
    global available_balance
    available_balance -= amount

def get_available_balance():
    return available_balance
