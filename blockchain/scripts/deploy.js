async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with:", deployer.address);

  const Cert = await ethers.getContractFactory("CertificateRegistry");
  const cert = await Cert.deploy();
  await cert.deployed();

  console.log("CertificateRegistry deployed to:", cert.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
