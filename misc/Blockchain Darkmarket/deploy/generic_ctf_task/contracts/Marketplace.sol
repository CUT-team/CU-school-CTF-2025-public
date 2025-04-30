// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

contract Marketplace {
    address public owner;

    struct Product {
        uint256 id;
        string name;
        uint256 price;
        bool isAvailable;
    }

    uint256 public productCounter;
    mapping(uint256 => Product) public products;
    mapping(address => uint256) public balances;
    mapping(address => mapping(uint256 => bool)) public purchases;
    mapping(uint256 => string) private productContents;

    event ProductCreated(uint256 id, string name, uint256 price);
    event ProductPurchased(uint256 id, address buyer);
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the marketplace owner can perform this action");
        _;
    }

    constructor(address _owner) {
        owner = _owner;
    }

    function createProduct(string memory name, uint256 price, string memory itemContent) external onlyOwner {
        require(price > 0, "Price must be greater than zero");
        productCounter++;
        products[productCounter] = Product({
            id: productCounter,
            name: name,
            price: price,
            isAvailable: true
        });
        productContents[productCounter] = itemContent;        
        emit ProductCreated(productCounter, name, price);
    }

    function purchaseProduct(uint256 productId) external {
        Product storage product = products[productId];
        require(product.isAvailable, "Product is not available");
        require(balances[msg.sender] >= product.price, "Insufficient balance");
        balances[msg.sender] -= product.price;
        balances[owner] += product.price;
        purchases[msg.sender][productId] = true;
        emit ProductPurchased(productId, msg.sender);
    }

    function getPurchasedItem(uint256 productId) external view returns (string memory) {
        require(purchases[msg.sender][productId], "You did not purchase this product");
        return productContents[productId];
    }

    function deposit() external payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw() external {
        require(balances[msg.sender] > 0, "Insufficient balance");
        (bool success, ) = msg.sender.call{value: balances[msg.sender]}("");
        require(success, "Transfer failed");
        balances[msg.sender] = 0;
        emit Withdrawal(msg.sender);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "New owner cannot be the zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}
