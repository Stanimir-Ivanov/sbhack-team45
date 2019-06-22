from src.contracts.hello_world import HelloWorld
from flask import Flask

#####################
# Contracts and utils definitions
#####################

# Read contract source and instantiate a util object to interact with the contract
with open('solidity/hello_world.sol', 'r') as file:
    data = file.read()

hello_world_contract = HelloWorld(
    provider='http://127.0.0.1:7545',
    contract_source=data,
    contract_name="Greeter",
    contract_address="0x0652eCde3070e77093e1d8C36fd08C9807Ba158c"
)

######################
# API endpoint - routes
######################

# Create the application instance
app = Flask(__name__, template_folder="templates")


# Call function greet from defined contract
@app.route('/api/greet')
def callContract():
    return hello_world_contract.greet()


if __name__ == '__main__':
    app.run(debug=True)
