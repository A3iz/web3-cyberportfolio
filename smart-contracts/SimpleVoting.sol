// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SimpleVoting
 * @dev A secure voting contract demonstrating Web3 security principles
 * @author Abdulaziz Althari
 */
contract SimpleVoting {
    struct Proposal {
        string description;
        uint256 voteCount;
        bool active;
        mapping(address => bool) hasVoted;
    }

    address public owner;
    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    mapping(address => bool) public authorizedVoters;
    
    event ProposalCreated(uint256 indexed proposalId, string description);
    event VoteCast(uint256 indexed proposalId, address indexed voter);
    event ProposalEnded(uint256 indexed proposalId, uint256 finalVoteCount);
    event VoterAuthorized(address indexed voter);
    event VoterRevoked(address indexed voter);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyAuthorizedVoter() {
        require(authorizedVoters[msg.sender], "Voter not authorized");
        _;
    }

    modifier validProposal(uint256 _proposalId) {
        require(_proposalId < proposalCount, "Proposal does not exist");
        require(proposals[_proposalId].active, "Proposal is not active");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedVoters[msg.sender] = true;
        emit VoterAuthorized(msg.sender);
    }

    /**
     * @dev Create a new proposal
     * @param _description Description of the proposal
     */
    function createProposal(string memory _description) external onlyOwner {
        require(bytes(_description).length > 0, "Description cannot be empty");
        
        uint256 proposalId = proposalCount;
        Proposal storage newProposal = proposals[proposalId];
        newProposal.description = _description;
        newProposal.voteCount = 0;
        newProposal.active = true;
        
        proposalCount++;
        emit ProposalCreated(proposalId, _description);
    }

    /**
     * @dev Authorize a voter
     * @param _voter Address to authorize
     */
    function authorizeVoter(address _voter) external onlyOwner {
        require(_voter != address(0), "Invalid voter address");
        require(!authorizedVoters[_voter], "Voter already authorized");
        
        authorizedVoters[_voter] = true;
        emit VoterAuthorized(_voter);
    }

    /**
     * @dev Revoke voter authorization
     * @param _voter Address to revoke
     */
    function revokeVoter(address _voter) external onlyOwner {
        require(authorizedVoters[_voter], "Voter not authorized");
        require(_voter != owner, "Cannot revoke owner");
        
        authorizedVoters[_voter] = false;
        emit VoterRevoked(_voter);
    }

    /**
     * @dev Cast a vote on a proposal
     * @param _proposalId ID of the proposal to vote on
     */
    function vote(uint256 _proposalId) external onlyAuthorizedVoter validProposal(_proposalId) {
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.hasVoted[msg.sender], "Already voted on this proposal");
        
        proposal.hasVoted[msg.sender] = true;
        proposal.voteCount++;
        
        emit VoteCast(_proposalId, msg.sender);
    }

    /**
     * @dev End a proposal (only owner)
     * @param _proposalId ID of the proposal to end
     */
    function endProposal(uint256 _proposalId) external onlyOwner {
        require(_proposalId < proposalCount, "Proposal does not exist");
        require(proposals[_proposalId].active, "Proposal already ended");
        
        proposals[_proposalId].active = false;
        emit ProposalEnded(_proposalId, proposals[_proposalId].voteCount);
    }

    /**
     * @dev Get proposal details
     * @param _proposalId ID of the proposal
     * @return description Description of the proposal
     * @return voteCount Number of votes received
     * @return active Whether the proposal is active
     */
    function getProposal(uint256 _proposalId) external view returns (
        string memory description,
        uint256 voteCount,
        bool active
    ) {
        require(_proposalId < proposalCount, "Proposal does not exist");
        
        Proposal storage proposal = proposals[_proposalId];
        return (proposal.description, proposal.voteCount, proposal.active);
    }

    /**
     * @dev Check if an address has voted on a specific proposal
     * @param _proposalId ID of the proposal
     * @param _voter Address to check
     * @return Whether the voter has voted
     */
    function hasVoted(uint256 _proposalId, address _voter) external view returns (bool) {
        require(_proposalId < proposalCount, "Proposal does not exist");
        return proposals[_proposalId].hasVoted[_voter];
    }

    /**
     * @dev Get total number of proposals
     * @return Total proposal count
     */
    function getTotalProposals() external view returns (uint256) {
        return proposalCount;
    }
}
