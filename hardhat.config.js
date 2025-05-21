require("@nomicfoundation/hardhat-toolbox");
require("solidity-coverage");
require("hardhat-deploy");


const PRIVATE_KEY = "0x0000000000000000000000000000000000000000000000000000000000000000";


/** @type import("hardhat/config").HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.27",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  namedAccounts: {
    deployer: `privatekey://${PRIVATE_KEY}`,
  },
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      allowUnlimitedContractSize: true,
    },
    ronin: {
      chainId: 2020,
      url: "https://api.roninchain.com/rpc",
      gasPrice: 21_000_000_000,
      accounts: [PRIVATE_KEY],
    },
    saigon: {
      chainId: 2021,
      url: "https://saigon-testnet.roninchain.com/rpc",
      gasPrice: 21_000_000_000,
      accounts: [PRIVATE_KEY],
    }
  },
  sourcify: {
    enabled: true
  }
};