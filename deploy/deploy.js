const func = async function (hre) {
    const { deployments, getNamedAccounts } = hre;
    const { deploy } = deployments;

    const { deployer } = await getNamedAccounts();
    console.log("[INFO] Deploying contract with the account:", deployer);

    try {
        const mockTokenContract = await deploy("ERC20Mock", {
            from: deployer,
            args: [],
            log: true,
            gasPrice: 30000000000
        });

        await deploy("TokenBatchTransfer", {
            from: deployer,
            args: [
                mockTokenContract.address
                // "0x253ef7651433ca9ca5de487e1661a27080e85a83" // SAIGON PIXEL 
                // "0x7eae20d11ef8c779433eb24503def900b9d28ad7" // RONIN PIXEL 
            ],
            log: true,
            gasPrice: 30000000000
        });

    } catch (error) {
        console.error("[ERROR] Error deploying contract:", error);
    }
};

module.exports = func;
func.tags = ["TokenBatchTransfer"];
