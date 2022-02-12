pragma solidity >=0.5.0 < 0.9.0;

contract B {
        event EventB(string indexed name);
        event ttt(bool tff);
        function get() payable public {
                (bool ok, ) = msg.sender.call.value(1 ether)("");
		if(ok) return;
		if(ok==0) return;
		if(ok==0 && True) return;
		require(ok);
		require(ok,"pass");
		require(ok==True);
//                msg.sender.call.value(2 ether)("");


//(bool sent, ) = msg.sender.call{value:msg.value}("");
}
function getBalance() public view returns (uint256) {
return address(this).balance;
}
}

