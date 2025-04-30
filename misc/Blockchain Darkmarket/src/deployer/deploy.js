const { ethers } = require('ethers');
const fs = require('fs');
const express = require('express');

const factoryABI = JSON.parse(fs.readFileSync('./build/ProductFactory.abi', 'utf8'));
const factoryBytecode = fs.readFileSync('./build/ProductFactory.bin', 'utf8');
const MarketplaceABI = JSON.parse(fs.readFileSync('./build/Marketplace.abi', 'utf8'));

const RPC_URL = process.env.RPC_URL || 'http://127.0.0.1:7545';
const provider = new ethers.JsonRpcProvider(RPC_URL);

const ACCOUNT1_PRIVATEKEY = process.env.ACCOUNT1.split(',')[0];
const ACCOUNT2_PRIVATEKEY = process.env.ACCOUNT2.split(',')[0];

const app = express();
app.use(express.json());

let participantPrivateKey = '';
let marketplaceAddress = '';

async function deployContracts() {
  const wallet1 = new ethers.Wallet(ACCOUNT1_PRIVATEKEY, provider);
  console.log(`Using deployer account: ${wallet1.address}`);

  const wallet2 = new ethers.Wallet(ACCOUNT2_PRIVATEKEY, provider);
  console.log(`Participant account: ${wallet2.address}`);
  console.log(`Participant private key: ${wallet2.privateKey}`);
  console.log(`Participant balance: ${await provider.getBalance(wallet2.address)}`);

  const Factory = new ethers.ContractFactory(factoryABI, factoryBytecode, wallet1);
  const factory = await Factory.deploy();

  marketplaceAddress = await factory.getMarketplaceAddress();

  console.log(`ProductFactory deployed at: ${factory.target}`);
  console.log(`Marketplace deployed at: ${marketplaceAddress}`);

  const contract = new ethers.Contract(marketplaceAddress, MarketplaceABI, wallet1);

  const tx2 = await contract.deposit({
    value: ethers.parseEther("1000000.0"),
  });
  await tx2.wait();
  console.log(`Funded Marketplace contract with 1000000 ETH`);

  participantPrivateKey = wallet2.privateKey;
}

app.get('/', (req, res) => {
  res.json({
    privateKey: participantPrivateKey,
    marketplaceAddress: marketplaceAddress,
    RPC_PORT: 8545,
  });
});

deployContracts().catch(console.error);

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
