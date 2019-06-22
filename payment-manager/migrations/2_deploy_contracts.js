var PaymentManager = artifacts.require("PaymentManager");

module.exports = function(deployer){
  deployer.deploy(PaymentManager);
};
