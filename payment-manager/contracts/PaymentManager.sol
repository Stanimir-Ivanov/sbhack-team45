pragma solidity 0.5.8;

contract PaymentManager {

    address owner;

    struct User {
        address payable referenceAddress;
        uint256 balance;
    }

    struct Provider {
        address payable referenceAddress;
        string name;
        uint256 balance;
        uint256 cost;
    }

    mapping(address => User) public usersData;
    address[] public users;
    uint256 totalUsers;

    mapping(address => Provider) public providersData;
    address[] public providers;
    uint256 totalProviders;

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

    modifier isOwner(address sender){
        require(sender==owner,
        "Only the contract owner may call this function");
        _;
    }

    constructor() public {
        owner = msg.sender;
        totalUsers = 0;
        totalProviders = 0;
    }

    // Adding user's address to global array
    function userSignup() public userNotSignedUp(msg.sender) {
        usersData[msg.sender].referenceAddress = msg.sender;
        usersData[msg.sender].balance = 0;
        totalUsers++;
    }

    // Same but for the provider
    function providerSignUp(uint256 cost, string memory name) public providerNotSignedUp(msg.sender) {
        providersData[msg.sender].referenceAddress = msg.sender;
        providersData[msg.sender].balance = 0;
        providersData[msg.sender].cost = cost;
        providersData[msg.sender].name = name;
        totalProviders++;
    }
    
    // Top up
    function userTopUp() public userSignedUp(msg.sender) payable {
        usersData[msg.sender].balance += msg.value;
    }

    function userWithdraw(uint256 value) public userSignedUp(msg.sender) payable {
        if(usersData[msg.sender].balance >= value){
            usersData[msg.sender].balance -= value;
            msg.sender.transfer(value);
        }
    }

    // Provider gets his money
    function providerWithdraw(uint256 value) public providerSignedUp(msg.sender)  payable {
        if(providersData[msg.sender].balance >= value){
            providersData[msg.sender].balance -= value;
            msg.sender.transfer(value);
        }
    }

    // Send all outstanding balances to providers
    function sendAllProviderBalances() public isOwner(msg.sender) payable {
        for(uint256 i = 0; i < totalUsers; i++){
            providersData[providers[i]].referenceAddress.transfer(providersData[providers[i]].balance);
            providersData[providers[i]].balance = 0;
        }
    }

    // Update the balances for both users and providers
    function userPayForTrip(address providerAddress) public userSignedUp(msg.sender) providerSignedUp(providerAddress) {
        providersData[providerAddress].balance += providersData[providerAddress].cost;
        usersData[msg.sender].balance -= providersData[providerAddress].cost;
    }

    function getUserBalance() public view userSignedUp(msg.sender) returns (uint256 ret) {
        return usersData[msg.sender].balance;
    }

    function getProviderBalance() public view providerSignedUp(msg.sender) returns (uint256 ret) {
        return providersData[msg.sender].balance;
    }

    function setProviderCost(uint256 cost) public providerSignedUp(msg.sender) {
        providersData[msg.sender].cost = cost;
    }

    function getProviderCost() public view providerSignedUp(msg.sender) returns (uint256 ret) {
        return providersData[msg.sender].cost;
    }

    function getProviderData(address providerAddress) public view providerSignedUp(msg.sender) returns (string memory name, uint256 cost) {
        name = providersData[providerAddress].name;
        cost = providersData[providerAddress].cost;
    }

}