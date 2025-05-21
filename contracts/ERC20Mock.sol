//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Mock is ERC20 {
    uint8 private immutable _customDecimals;

    constructor() ERC20("ERC20Mock", "ERC20M") {
        _customDecimals = 18;
    }

    function decimals() public view override returns (uint8) {
        return _customDecimals;
    }

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }
}
