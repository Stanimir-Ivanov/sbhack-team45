from eth_account import Account

from src.utils.utils import Utils


class PaymentManager:
    def __init__(self, provider, contract_source, contract_name, contract_address, private_key):
        super(PaymentManager, self).__init__()

        # Retrieves an interface to the contract
        contract_interface = Utils.get_contract_interface(contract_source, contract_name)
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
        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.userSignup().transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            # raise Warning("Oups. Somethings went wrong")
            return "User already signed up"

    def signup_provider(self, cost):
        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.providerSignUp(cost).transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            return "Provider already signed up"

    def top_up(self, amount):
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
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def withdraw(self, amount):
        try:
            if self.utils.get_provider().isConnected():
                self.contract.functions.providerWithdraw(amount).call()
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def pay(self, to_provider):
        try:
            if self.utils.get_provider().isConnected():
                self.utils.get_provider().eth.defaultAccount = \
                    Account.privateKeyToAccount(self.private_key).address
                hash = self.contract.functions.userPayForTrip(to_provider).transact()
                # Wait for transaction to be mined...
                self.utils.get_provider().eth.waitForTransactionReceipt(hash)
                return ""
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def get_balance_user(self):
        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getUserBalance().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def get_balance_provider(self):
        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getProviderBalance().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def get_cost_provider(self):
        try:
            if self.utils.get_provider().isConnected():
                return self.contract.functions.getProviderCost().call()
            else:
                raise Warning("Couldn't connect to the provider")
        except:
            raise Warning("Oups. Something went wrong")

    def set_cost_provider(self, cost):
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
            raise Warning("Oups. Something went wrong")
