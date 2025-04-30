// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

import "./Marketplace.sol";

contract ProductFactory {
    address private owner;
    Marketplace private marketplace;

    event MarketplaceCreated(address marketplaceAddress);
    event DefaultProductsCreated(address marketplaceAddress);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the factory owner can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
        marketplace = new Marketplace(address(this));
        emit MarketplaceCreated(address(marketplace));
        string[11] memory defaultNames = [
            "Exploit Generator 3000",
            "Elite Hacker Hoodie",
            "Ultimate Phishing Kit",
            "Zero-Day Finder",
            "Firewall Bypass Guide",
            "DDoS Attack Simulator",
            "Top-Secret VPN",
            "Malware DIY Kit",
            "Social Engineering 101",
            "Cybersecurity Troll Stickers",
            "FLAG"
        ];

        uint80[11] memory defaultPrices = [
            0.5 ether,
            0.3 ether,
            0.8 ether,
            1 ether,
            0.6 ether,
            0.4 ether,
            0.7 ether,
            0.9 ether,
            0.2 ether,
            0.1 ether,
            10000 ether
        ];

        string[11] memory defaultContents = [
            "Link to exploit generator: https://exploit.gen",
            "Elite hacker hoodie available here: https://hoodie.shop",
            "Phishing guide: https://phishing.kit",
            "Zero-day finder: https://zero-day.tool",
            "Firewall bypass guide: https://firewall.guide",
            "DDoS simulator download: https://ddos.sim",
            "VPN configuration: https://vpn.config",
            "DIY malware kit: https://malware.diy",
            "Social engineering tricks: https://social.tricks",
            "Cybersecurity stickers: https://stickers.shop",
            "cuctf{3xpl01t3d_Re3ntrancy_Attack}"
        ];

        for (uint256 i = 0; i < 11; i++) {
            marketplace.createProduct(defaultNames[i], defaultPrices[i], defaultContents[i]);
        }

        marketplace.transferOwnership(msg.sender);
    }

    function getMarketplaceAddress() public view returns (address){
        return address(marketplace);
    }
}