// SPDX-License-Identifier:GPL-30

pragma solidity >=0.5.0 <0.9.0;

contract FibonacciBalance{
   

    address public fibonacciLibrary;

    uint public calculatedFibNumber;

    uint public start = 3;

    uint public withdrawalCounter;

    constructor(address _fibonacciLibrary) public{

        fibonacciLibrary = _fibonacciLibrary;

    }

    function withdraw() public{

        withdrawalCounter +=1;

        (bool success, bytes memory data) =fibonacciLibrary.delegatecall(abi.encodeWithSignature("setFibonacci(uint256)",withdrawalCounter));

        msg.sender.transfer(calculatedFibNumber * 1 ether);

    }



}
