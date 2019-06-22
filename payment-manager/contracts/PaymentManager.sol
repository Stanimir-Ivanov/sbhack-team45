pragma solidity 0.5.9;

contract PaymentManager {

    struct User {
        address referenceAddress;
        uint256 balance;
    }

    struct Provider {
        address referenceAddress;
        uint256 balance;
        uint256 cost;
    }

    mapping(address => User) public usersData;
    mapping(address => Provider) public providersData;

    modifier userSignedUp(address sender){
        require(usersData[sender].referenceAddress != address(0),
        "User not signed up");
        _;
    }

    modifier userNotSignedUp(address sender){
        require(usersData[sender].referenceAddress == address(0),
        "User already signed up");
        _;
    }

    modifier providerSignedUp(address sender){
        require(providersData[sender].referenceAddress != address(0),
        "Provider not signed up");
        _;
    }

    modifier providerNotSignedUp(address sender){
        require(providersData[sender].referenceAddress == address(0),
        "Provider already signed up");
        _;
    }

    constructor() public {

    }

    // Adding user's address to global array
    function userSignup() public userNotSignedUp(msg.sender) {
        usersData[msg.sender].referenceAddress = msg.sender;
        usersData[msg.sender].balance = 0;
    }

    // Same but for the provider
    function providerSignUp(uint256 cost) public providerNotSignedUp(msg.sender)  {
        providersData[msg.sender].referenceAddress = msg.sender;
        providersData[msg.sender].balance = 0;
        providersData[msg.sender].cost = cost;
    }
    
    // Top up
    function userTopUp() public payable userSignedUp(msg.sender) {
        usersData[msg.sender].balance += msg.value;
    }

    // Provider gets his money
    function providerWithdraw(uint256 value) public providerSignedUp(msg.sender)  payable {
        if(providersData[msg.sender].balance >= value){
            providersData[msg.sender].balance -= value;
            msg.sender.transfer(value);
        }
    }

    // Update the balances for both users and providers
    function userPayForTrip(address providerAddress) public userSignedUp(msg.sender) providerSignedUp(providerAddress) {
        providersData[providerAddress].balance += providersData[providerAddress].cost;
        usersData[msg.sender].balance -= providersData[providerAddress].cost;
    }

    function getUserBalance(address userAddress) public userSignedUp(userAddress) {
        return usersData[userAddress].balance;
    }

    function getProviderBalance(address providerAddress) public providerSignedUp(providerAddress) {
        return providersData[providerAddress].balance;
    }

    function setProviderCost(uint256 cost) public providerSignedUp(msg.sender) {
        providersData[msg.sender].cost = cost;
    }

    function getProviderCost(address providerAddress) public providerSignedUp(providerAddress) {
        return providersData[providerAddress].cost;
    }



}