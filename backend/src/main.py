import json

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
    contract_address="0xd248046634cAb7De1bF07aD49ceAFA0894AeDe79",
    private_key="0x7864fd5e9c48c258cfc93972a2b8de72b617b897fa01b745bec32c380d67a7dc"
)

######################
# API endpoint - routes
######################

# Create the application instance
app = Flask(__name__, template_folder="templates")


@app.route('/api/user_signup')
def user_sign_up():
    return payment_manager_contract.signup_user()


@app.route('/api/provider_signup')
def provider_sign_up():
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
    return str(payment_manager_contract.get_balance_user())


@app.route('/api/getBalanceProvider')
def get_balance_provider():
    return payment_manager_contract.get_balance_provider()


@app.route('/api/getCostProvider')
def get_cost_provider():
    return payment_manager_contract.get_cost_provider()


@app.route('/api/setCostProvider')
def set_cost_provider():
    cost = request.args.get('cost')
    if cost is not None:
        return payment_manager_contract.set_cost_provider(cost)
    else:
        return "404 - Error - Not found: bad PUT parameter"


if __name__ == '__main__':
    app.run(debug=True)
