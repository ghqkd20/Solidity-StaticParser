// SPDX-License-Identifier:GPL-30

pragma solidity >=0.7.0 <0.9.0;


contract intt{


    mapping (address => uint) public balance;

    function transferProxy(address from, address to, uint value, uint fee) public {
        if (balance[from]<fee+value) revert();

        if (balance[to]+value <balance[to] || balance[msg.sender] + fee <balance[msg.sender]) revert();
        balance[to] +=value;
        balance[msg.sender] += fee;
        balance[from] -= value + fee;
    }
}
