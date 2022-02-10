// SPDX-License-Identifier:GPL-30

pragma solidity >=0.5.0 <0.9.0;



contract testLL{

    uint constant LARGEGAS = 100000;

    address addrArr;

    function LongList(uint256 nextV, uint[] memory arr, address _addr) public { 
        addrArr = _addr;

        for(uint256 i = nextV;i<arr.length; i++){

            addrArr.send(arr[i]);

        }

    }

}
