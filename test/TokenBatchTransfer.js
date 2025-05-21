const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("📝 TokenBatchTransfer", function () {
  let token, batchTransfer; //, owner, addr1, addr2, addr3;

  beforeEach(async function () {
    [ owner, addr1, addr2, addr3 ] = await ethers.getSigners();

    // Deploy mock ERC20 token
    const ERC20Mock = await ethers.getContractFactory("ERC20Mock");
    token = await ERC20Mock.deploy();
    await token.waitForDeployment();
    tokenAddress = await token.getAddress();

    // Deploy batch transfer contract
    const TokenBatchTransfer = await ethers.getContractFactory("TokenBatchTransfer");
    batchTransfer = await TokenBatchTransfer.deploy(tokenAddress);
    await batchTransfer.waitForDeployment();
    batchTransferAddress = await batchTransfer.getAddress();

    // Mint and transfer some tokens to the batch contract
    await token.mint(owner, ethers.parseEther("1000"));
    await token.transfer(batchTransferAddress, ethers.parseEther("500"));
  });

  it("🔥 Should deploy correctly with correct owner and vault", async function () {
    expect(await batchTransfer.owner()).to.equal(owner.address);
    expect(await batchTransfer.vaultAddress()).to.equal(owner.address);
  });

  it("🔥 Should calculate sum correctly", async function () {
    const sum = await batchTransfer.sum([100, 200, 300]);
    expect(sum).to.equal(600);
  });

  it("🔥 Should batch transfer tokens", async function () {
    const holders = [ addr1.address, addr2.address ];
    const amounts = [ ethers.parseEther("10"), ethers.parseEther("15") ];

    // Verify before transfers
    expect(await token.balanceOf(addr1.address)).to.equal(0);
    expect(await token.balanceOf(addr2.address)).to.equal(0);

    // Transfer tokens
    await batchTransfer.batchTransfer(holders, amounts);

    // Verify transfers
    expect(await token.balanceOf(addr1.address)).to.equal(amounts[0]);
    expect(await token.balanceOf(addr2.address)).to.equal(amounts[1]);
  });

  it("🔥 Should revert batch transfer if arrays mismatch", async function () {
    const holders = [ addr1.address ];
    const amounts = [ ethers.parseEther("10"), ethers.parseEther("15") ];

    await expect(
        batchTransfer.batchTransfer(holders, amounts)
    ).to.be.revertedWith("Lengths of arrays do not match");
  });

  it("🔥 Should revert batch transfer if there's insufficient balance", async function () {
    const holders = [ addr1.address ];
    const amounts = [ ethers.parseEther("1000") ]; // More than balance

    await expect(
        batchTransfer.batchTransfer(holders, amounts)
    ).to.be.revertedWith("Not enough balance in the contract");
  });

  it("🔥 Should withdraw a specific amount", async function () {
    const withdrawAmount = ethers.parseEther("50");

    await batchTransfer.withdrawToken(withdrawAmount);

    expect(await token.balanceOf(owner.address)).to.equal(
      ethers.parseEther("550") // 500 initial + 50 withdrawn
    );
  });

  it("🔥 Should revert withdrawToken on invalid amount", async function () {
    await expect(
        batchTransfer.withdrawToken(0)
    ).to.be.revertedWith("Amount must be greater than 0");
    
    await expect(
        batchTransfer.withdrawToken(ethers.parseEther("1000"))
    ).to.be.revertedWith("Insufficient contract balance");
  });

  it("🔥 Should withdraw all tokens", async function () {
    const contractBalance = await token.balanceOf(batchTransferAddress);

    await batchTransfer.withdrawAllToken();

    expect(await token.balanceOf(batchTransferAddress)).to.equal(0);
    expect(await token.balanceOf(owner.address)).to.equal(ethers.parseEther("1000"));
  });
});
