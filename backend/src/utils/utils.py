from solc import compile_standard
from web3 import Web3
from web3.auto import w3


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
        return self.w3

    def get_contract(self, address, abi):
        """
        Returns a contract object by its address
        :return: a contract instance
        """

        return self.w3.eth.contract(address=address, abi=abi)
