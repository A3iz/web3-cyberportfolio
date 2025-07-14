# SimpleVoting Smart Contract

## Overview
`SimpleVoting.sol` is a secure voting smart contract that demonstrates Web3 security best practices. It implements a permission-based voting system with proper access controls and event logging.

## Features
- **Secure Voting**: Each authorized voter can vote only once per proposal
- **Access Control**: Owner-managed voter authorization system
- **Event Logging**: All actions are logged via events for transparency
- **Proposal Management**: Create, manage, and end voting proposals
- **Input Validation**: Comprehensive validation to prevent common vulnerabilities

## Contract Functions

### Owner Functions
- `createProposal(string _description)`: Create a new voting proposal
- `authorizeVoter(address _voter)`: Authorize an address to vote
- `revokeVoter(address _voter)`: Revoke voting authorization
- `endProposal(uint256 _proposalId)`: End an active proposal

### Voter Functions
- `vote(uint256 _proposalId)`: Cast a vote on an active proposal

### View Functions
- `getProposal(uint256 _proposalId)`: Get proposal details
- `hasVoted(uint256 _proposalId, address _voter)`: Check if address has voted
- `getTotalProposals()`: Get total number of proposals

## Security Features
- **Reentrancy Protection**: No external calls that could lead to reentrancy
- **Access Modifiers**: Proper function access control
- **Input Validation**: Comprehensive parameter validation
- **Double-voting Prevention**: Mapping tracks voting status per address
- **Owner Protection**: Owner cannot be revoked from voting

## Deployment & Testing

### Using Remix IDE
1. Open [Remix IDE](https://remix.ethereum.org/)
2. Create a new file and paste the contract code
3. Compile with Solidity version `^0.8.19`
4. Deploy to your preferred testnet (Sepolia, Goerli)
5. Interact with the contract using Remix interface

### Using Hardhat
```bash
# Install Hardhat
npm install --save-dev hardhat

# Initialize Hardhat project
npx hardhat

# Add the contract to contracts/SimpleVoting.sol
# Create deployment script in scripts/deploy.js

# Deploy to local network
npx hardhat run scripts/deploy.js --network localhost

# Deploy to testnet
npx hardhat run scripts/deploy.js --network sepolia
```

### Sample Deployment Script (deploy.js)
```javascript
const { ethers } = require("hardhat");

async function main() {
  const SimpleVoting = await ethers.getContractFactory("SimpleVoting");
  const voting = await SimpleVoting.deploy();
  
  await voting.deployed();
  console.log("SimpleVoting deployed to:", voting.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

## Gas Optimization
- Uses `uint256` for efficient storage
- Minimal external calls
- Efficient mapping structures
- Event emission for off-chain tracking

## Security Considerations
- Always test on testnet before mainnet deployment
- Consider adding time-based voting periods
- Implement proposal threshold requirements for production use
- Add emergency pause functionality for critical situations

## License
MIT License - See contract header for details
