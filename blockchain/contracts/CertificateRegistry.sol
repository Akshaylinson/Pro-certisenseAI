// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateRegistry {
    struct Record {
        address issuer;
        uint256 timestamp;
    }

    // store hash -> Record
    mapping(bytes32 => Record) public records;
    event CertificateStored(bytes32 indexed hash, address indexed issuer, uint256 timestamp);

    /// @notice store certificate hash; idempotent (won't overwrite existing)
    function store(bytes32 certHash) external {
        require(certHash != bytes32(0), "Invalid hash");
        if (records[certHash].timestamp == 0) {
            records[certHash] = Record({
                issuer: msg.sender,
                timestamp: block.timestamp
            });
            emit CertificateStored(certHash, msg.sender, block.timestamp);
        }
    }

    /// @notice returns (issuer, timestamp) if stored, timestamp==0 means not stored
    function get(bytes32 certHash) external view returns (address issuer, uint256 timestamp) {
        Record memory r = records[certHash];
        return (r.issuer, r.timestamp);
    }
}
