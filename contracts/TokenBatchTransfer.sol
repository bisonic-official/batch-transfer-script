//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TokenBatchTransfer is Ownable {
    /**
     * @notice The token contract address.
     * @notice Must be set during deployment.
     */
    IERC20 public token;

    /**
     * @notice Vault address.
     * @notice This address will receive all the funds after withdrawal.
     */
    address public vaultAddress;

    /**
     * @dev Event to be emited on token withdrawal.
     * @param sender address The address of the sender.
     * @param amount unit256 The amount withdrawn.
     */
    event WithdrawToken(address indexed sender, uint256 amount);

    /**
     * @dev Event to be emited on token batch transfer.
     * @param sender address The address of the sender.
     * @param recipients address[] The address of the holders.
     * @param amounts unit256[] The amounts sent.
     */
    event BatchTransfer(
        address indexed sender,
        address[] recipients,
        uint256[] amounts
    );

    /**
     * @dev Constructor function.
     * @param _token address The address of the token contract.
     */
    constructor(address _token) Ownable(msg.sender) {
        // Set the token contract address
        token = IERC20(_token);

        // Set the owner and vaultAddress as the contract creator
        vaultAddress = payable(msg.sender);
    }

    /**
     * @dev Set the vault address.
     * @param _vaultAdress address The address of the vault.
     */
    function setVaultAddress(address _vaultAdress) external onlyOwner {
        vaultAddress = payable(_vaultAdress);
    }

    /**
     * @dev Function to return the sum of an array of uint256.
     * @param amounts uint256[] The list of amount per address to transfer.
     */
    function sum(uint256[] memory amounts) public pure returns (uint256 total) {
        for (uint256 i = 0; i < amounts.length; i++) {
            // Solidity 0.8+ prevents overflow automatically
            total += amounts[i];
        }
    }

    /**
     * @dev Function to transfer tokens from contract to the provided list
     * of token holders with respective amount.
     * @param tokenHolders address[] The list of addresses to transfer token.
     * @param amounts uint256[] The list of amount per address to transfer.
     */
    function batchTransfer(
        address[] calldata tokenHolders,
        uint256[] calldata amounts
    ) external onlyOwner {
        // Validate array lengths
        require(
            tokenHolders.length == amounts.length,
            "Lengths of arrays do not match"
        );

        // Check if contract has the required balance
        uint256 totalAmount = sum(amounts);
        require(
            token.balanceOf(address(this)) >= totalAmount,
            "Not enough balance in the contract"
        );

        // Transfer token to holders
        for (uint256 index = 0; index < tokenHolders.length; index++) {
            require(
                token.transfer(tokenHolders[index], amounts[index]),
                "Unable to transfer token to the account"
            );
        }

        // Emit batch transfer event
        emit BatchTransfer(msg.sender, tokenHolders, amounts);
    }

    /**
     * @dev Withdraw funds to the vault using transferFrom.
     * @param _amount uint256 The amount to withdraw.
     */
    function withdrawToken(uint256 _amount) external onlyOwner {
        uint256 pixelBalance = token.balanceOf(address(this));
        require(_amount > 0, "Amount must be greater than 0");
        require(_amount <= pixelBalance, "Insufficient contract balance");

        // Transfer token to vault address
        bool success = token.transfer(vaultAddress, _amount);

        require(success, "Withdraw was not successful");

        // Emit withdrawal event
        emit WithdrawToken(msg.sender, _amount);
    }

    /**
     * @dev Withdraw all the PIXEL funds to the vaultAdress using call.
     */
    function withdrawAllToken() external onlyOwner {
        uint256 _amount = token.balanceOf(address(this));
        require(_amount > 0, "Amount must be greater than 0");

        // Transfer token to vault address
        bool success = token.transfer(vaultAddress, _amount);

        require(success, "Withdraw all was not successful");

        // Emit withdrawal event
        emit WithdrawToken(msg.sender, _amount);
    }
}
