from flask import Flask, request

#####################
# Contracts and utils definitions
#####################

# Read contract source and instantiate a util object to interact with the contract
from src.contracts.payment_manager import PaymentManager

with open('../../payment-manager/contracts/PaymentManager.sol', 'r') as file:
    payment_manager = file.read()

payment_manager_contract = PaymentManager(
    provider='http://3.120.6.183:8545',
    contract_source=payment_manager,
    contract_name="PaymentManager",
    contract_address="0xD6c476Ac63b4CA433fA1B9310f1D50b8D44AE571",
    private_key="0xf92be558b1dea9591078c452b9b215c8a088e80523a3c2ce50c10e3c96de2461"
)

######################
# API endpoint - routes
######################

# Create the application instance
app = Flask(__name__, template_folder="templates")


@app.route('/api/user_signup')
def sign_up():
    return payment_manager_contract.signup_user()


@app.route('/api/provider_signup')
def sign_up():
    cost = request.args.get('cost')
    if cost is not None:
        return payment_manager_contract.signup_provider(cost)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/topup')
def top_up():
    amount = request.args.get('amount')
    if amount is not None:
        return payment_manager_contract.top_up(amount)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/withdraw')
def withdraw():
    amount = request.args.get('amount')
    if amount is not None:
        return payment_manager_contract.withdraw(amount)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/pay')
def pay():
    to_provider = request.args.get('to')
    if to_provider is not None:
        return payment_manager_contract.pay(to_provider)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/getBalanceUser')
def get_balance_user():
    addr = request.args.get('addr')
    if addr is not None:
        return payment_manager_contract.get_balance_user(addr)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/getBalanceProvider')
def get_balance_provider():
    addr = request.args.get('addr')
    if addr is not None:
        return payment_manager_contract.get_balance_provider(addr)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/getCostProvider')
def get_balance_provider():
    addr = request.args.get('addr')
    if addr is not None:
        return payment_manager_contract.get_cost_provider(addr)
    else:
        return "404 - Error - Not found: bad GET parameter"


@app.route('/api/setCostProvider')
def get_balance_provider():
    cost = request.args.get('cost')
    if cost is not None:
        return payment_manager_contract.set_cost_provider(cost)
    else:
        return "404 - Error - Not found: bad PUT parameter"


if __name__ == '__main__':
    app.run(debug=True)
