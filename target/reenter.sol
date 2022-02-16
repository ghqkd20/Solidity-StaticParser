pragma solidity >=0.5.0 <0.9.0;

contract DAO{

    mapping(address=>uint256) public deposit;
    bool mutex1;
    bool mutex2 = false;
    function credit() public payable{
        deposit[msg.sender] += msg.value;
    }

    function getCreditedAmount(address) public returns(uint256){
        return deposit[msg.sender];
    }

    function withdraw(uint amount) public{
        bool mutex3;
        bool mutex4 = true;
        if(deposit[msg.sender] >=amount){
            msg.sender.call.value(amount)("");
            deposit[msg.sender] -= amount;
        }
    }
}
