from src.utils.utils import Utils


class HelloWorld:
    """
    Example class to show interactions between a solidity contract and python
    """

    def __init__(self, provider, contract_source, contract_name, contract_address):
        super(HelloWorld, self).__init__()

        # Retrieves an interface to the contract
        contract_interface = Utils.get_contract_interface(contract_source, contract_name)
        self.utils = Utils(provider=provider)

        # Makes sure the provider is reachable
        if not self.utils.isConnected():
            raise ValueError(f"Error: could not connect to {provider}")

        # Instantiate a contract object
        self.contract = self.utils.get_contract(contract_address, contract_interface['abi'])

    def greet(self):
        """
        This function calls the greet() method defined in hello_world.sol
        :return: the content of the greetings variable
        """

        return self.contract.functions.greet().call()
