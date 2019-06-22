pragma solidity 0.5.8;

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

    function userSignup() public userNotSignedUp(msg.sender) {
        usersData[msg.sender].referenceAddress = msg.sender;
        usersData[msg.sender].balance = 0;
    }

    function providerSignUp(uint256 cost) public providerNotSignedUp(msg.sender)  {
        providersData[msg.sender].referenceAddress = msg.sender;
        providersData[msg.sender].balance = 0;
        providersData[msg.sender].cost = cost;
    }
    
    function userTopUp() public payable userSignedUp(msg.sender) {
        usersData[msg.sender].balance += msg.value;
    }

    function providerWithdraw(uint256 value) public providerSignedUp(msg.sender)  payable {
        if(providersData[msg.sender].balance >= value){
            providersData[msg.sender].balance -= value;
            msg.sender.transfer(value);
        }
    }

    function userPayForTrip(address providerAddress) public userSignedUp(msg.sender) providerSignedUp(providerAddress) {
        providersData[providerAddress].balance += providersData[providerAddress].cost;
        usersData[msg.sender].balance -= providersData[providerAddress].cost;
    }

}