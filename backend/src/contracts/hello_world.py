from eth_account import Account

from src.utils.utils import Utils


class HelloWorld:
    """
    Example class to show interactions between a solidity contract and python
    """

    def __init__(self, provider, contract_source, contract_name, contract_address, private_key):
        super(HelloWorld, self).__init__()

        # Retrieves an interface to the contract
        contract_interface = Utils.get_contract_interface(contract_source, contract_name)
        self.utils = Utils(provider=provider)

        # Makes sure the provider is reachable
        if not self.utils.isConnected():
            raise ValueError(f"Error: could not connect to {provider}")

        # Instantiate a contract object
        self.contract = self.utils.get_contract(contract_address, contract_interface['abi'])

        self.private_key = private_key

    def greet(self):
        """
        This function calls the greet() method defined in hello_world.sol
        :return: the content of the greetings variable
        """

        return self.contract.functions.greet().call()

    def setGreet(self, greet):
        if self.utils.get_provider().isConnected():
            self.utils.get_provider().eth.defaultAccount = \
                Account.privateKeyToAccount(self.private_key).address
            hash = self.contract.functions.setGreeting(greet).transact()
            # Wait for transaction to be mined...
            self.utils.get_provider().eth.waitForTransactionReceipt(hash)
            return ""
