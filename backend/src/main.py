import json

from flask import Flask, request
from solc import compile_standard
from web3 import Web3
from web3.auto import w3
from eth_account import Account


class PaymentManager:
    def __init__(self, provider, contract_interface, contract_address, private_key):
        super(PaymentManager, self).__init__()

        # Retrieves an interface to the contract
        # contract_interface = Utils.get_contract_interface(contract_source, contract_name)
        self.utils = Utils(provider=provider)

        # Makes sure the provider is reachable
        if not self.utils.isConnected():
            raise ValueError(f"Error: could not connect to {provider}")

        # Instantiate a contract object
        if contract_address is not None:
            self.contract = self.utils.get_contract(contract_address, contract_interface['abi'])
        else:
            raise ValueError(f"Error: could not retrieve contract at address {contract_address}")

        self.private_key = private_key

    def signup_user(self):
        """
        Signs up a user
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.userSignup().transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def signup_provider(self, cost):
        """
        Signs up a provider and set its ticket cost
        :param cost: the cost of his service
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.providerSignUp(cost).transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def top_up(self, amount):
        """
        Puts money on a user account
        :param amount: the amount of token to deposit
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                self.contract.functions.userTopUp().transact(
                    {
                        'from': self.utils.get_provider().eth.defaultAccount,
                        'value': amount
                    }
                )
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def withdraw_provider(self, amount):
        """
        Allows a provider to withdraw money
        :param amount: the amount to withdraw
        """

        try:
            if self.utils.get_provider().isConnected():
                self.contract.functions.providerWithdraw(amount).call()
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def send_all_provider_balances(self):
        """
        Allows the contract owner to distribute all outstanding provider balances.
        The calling address must be contract owner (i.e. the address that constructed the contract)
        :param amount: the amount to withdraw
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.sendAllProviderBalances().transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def withdraw_user(self, amount):
        """
        Allows a user to withdraw money
        :param amount: the amount to withdraw
        """
        
        try:
            if self.utils.get_provider().isConnected():
                self.contract.functions.userWithdraw(amount).call()
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def pay(self, to_provider):
        """
        Sends money to the provider
        :param to_provider: the provider to which money needs to be sent
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.userPayForTrip(to_provider).transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return True
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def get_balance_user(self):
        """
        :return: the balance of the user
        """

        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getUserBalance().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def get_balance_provider(self):
        """
        :return: returns the balance of a provider
        """

        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getProviderBalance().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def get_cost_provider(self):
        """
        :return: the costs of the provider for his service
        """

        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getProviderCost().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False

    def set_cost_provider(self, cost):
        """
        Sets the provider's cost
        :param cost: the cost
        """

        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.setProviderCost(cost).transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return False


class Utils:
    """
    Utils class to interact with Ethereum blockchain
    @author Théo Giovanna - @SB Hack - 22/06/2019
    """

    def __init__(self, provider):
        super(Utils, self).__init__()
        self.provider = provider
        self.w3 = self._connect()

    def _connect(self):
        """
        Connect to the node provider
        :return: a Web3 instance
        """

        if self.provider is not None:
            return Web3(Web3.HTTPProvider(self.provider))
        else:
            raise ValueError("Provider cannot be nullWe")

    def isConnected(self):
        """
        Checks connection with the provider
        :return: True if connected, False otherwise
        """

        return self.w3.isConnected()

    @staticmethod
    def get_contract_interface(source, contractName):
        """
        Compiles solidity contract and return an interface to it
        :param source: the contract source code in .sol
        :param contractName: the contract name
        :return: its compiled version
        """

        compiled = compile_standard({
            "language": "Solidity",
            "sources": {
                "0": {
                    "content": source
                }
            },
            "settings": {
                "outputSelection": {"*": {"*": ["*"], "": ["*"]}}
            }
        })
        return compiled["contracts"]["0"][contractName]

    def get_provider(self):
        """
        :return: this instance's provider
        """

        return self.w3

    def get_contract(self, address, abi):
        """
        Returns a contract object by its address
        :return: a contract instance
        """

        return self.w3.eth.contract(address=address, abi=abi)


#####################
# Contracts and utils definitions
#####################

# Read contract source and instantiate a util object to interact with the contract
with open('../../payment-manager/build/contracts/PaymentManager.json', 'r') as json_file:
    contract_interface = json.load(json_file)

payment_manager_contract = PaymentManager(
    provider='http://127.0.0.1:7545',
    contract_interface=contract_interface,
    # contract_name="PaymentManager",
    contract_address="0x9F69E1c70c0d3616d78A2386056a8D8615C4ad90",
    private_key="fca1e2bfaff46a184e923a7db0937310cb267386f25b458c70c540fa7bc9472e"
)

######################
# API endpoint - routes
######################

# Create the application instance
app = Flask(__name__, template_folder="templates")


@app.route('/api/user_signup')
def user_sign_up():
    """
    Signs up a user to the contract
    :return: 200 if OK, 500 if error
    """
    if payment_manager_contract.signup_user():
        return json.dumps({'Response': '200 - OK'})
    else:
        return json.dumps({'Response': '500- Internal Server Error'})


@app.route('/api/provider_signup')
def provider_sign_up():
    """
    Signs up a provider to the contract
    :return: 200 if OK, 500 if error
    """

    cost = request.args.get('cost')
    if cost is not None:
        if payment_manager_contract.signup_provider(cost):
            return json.dumps({'Response': '200 - OK'})
        else:
            return json.dumps({'Response': '500- Internal Server Error'})
    else:
        return json.dumps({'Response': '400-Bad Request'})


@app.route('/api/topup')
def top_up():
    amount = request.args.get('amount')
    if amount is not None:
        if payment_manager_contract.top_up(amount):
            return json.dumps({'Response': '200 - OK'})
        else:
            return json.dumps({'Response': '500- Internal Server Error'})
    else:
        return json.dumps({'Response': '400-Bad Request'})


@app.route('/api/withdrawProvider')
def withdraw_provider():
    amount = request.args.get('amount')
    if amount is not None:
        if payment_manager_contract.withdraw_provider(amount):
            return json.dumps({'Response': '200 - OK'})
        else:
            return json.dumps({'Response': '500- Internal Server Error'})
    else:
        return json.dumps({'Response': '400-Bad Request'})

@app.route('/api/sendAllProviderBalances')
def send_all_provider_balances():    
    if payment_manager_contract.send_all_provider_balances():
        return json.dumps({'Response': '200 - OK'})
    else:
        return json.dumps({'Response': '500- Internal Server Error'})
    
@app.route('/api/withdrawUser')
def withdraw_user():
    amount = request.args.get('amount')
    if amount is not None:
        if payment_manager_contract.withdraw_user(amount):
            return json.dumps({'Response': '200 - OK'})
        else:
            return json.dumps({'Response': '500- Internal Server Error'})
    else:
        return json.dumps({'Response': '400-Bad Request'})


@app.route('/api/pay')
def pay():
    to_provider = request.args.get('to')
    if to_provider is not None:
        if payment_manager_contract.pay(to_provider):
            return json.dumps({'Response': '200 - OK'})
        else:
            return json.dumps({'Response': '500- Internal Server Error'})
    else:
        return json.dumps({'Response': '400-Bad Request'})


@app.route('/api/getBalanceUser')
def get_balance_user():
    balance = payment_manager_contract.get_balance_user()
    if balance is not None:
        return json.dumps({'Response': '200 - OK', 'Data:': str(balance)})
    else:
        return json.dumps({'Response': '500- Internal Server Error'})


@app.route('/api/getBalanceProvider')
def get_balance_provider():
    balance = payment_manager_contract.get_balance_provider()
    if balance is not None:
        return json.dumps({'Response': '200 - OK', 'Data:': str(balance)})
    else:
        return json.dumps({'Response': '500- Internal Server Error'})


@app.route('/api/getCostProvider')
def get_cost_provider():
    cost = payment_manager_contract.get_cost_provider()
    if cost is not None:
        return json.dumps({'Response': '200 - OK', 'Data:': str(cost)})
    else:
        return json.dumps({'Response': '500- Internal Server Error'})


@app.route('/api/setCostProvider')
def set_cost_provider():
    cost = request.args.get('cost')
    if cost is not None:
        return json.dumps({'Response': '200 - OK', 'Data:': str(cost)})
    else:
        return json.dumps({'Response': '400-Bad Request'})


if __name__ == '__main__':
    app.run(debug=True)
