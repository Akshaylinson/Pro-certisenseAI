const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("CertificateRegistry", function () {
  it("stores and returns certificate", async function () {
    const [owner, other] = await ethers.getSigners();
    const Cert = await ethers.getContractFactory("CertificateRegistry");
    const cert = await Cert.deploy();
    await cert.deployed();

    const hash = ethers.utils.sha256(ethers.utils.toUtf8Bytes("testpdf"));
    await cert.connect(owner).store(hash);

    const rec = await cert.get(hash);
    expect(rec.issuer).to.equal(owner.address);
    expect(rec.timestamp).to.be.gt(0);
  });

  it("idempotent store", async function () {
    const [owner] = await ethers.getSigners();
    const Cert = await ethers.getContractFactory("CertificateRegistry");
    const cert = await Cert.deploy();
    await cert.deployed();

    const hash = ethers.utils.sha256(ethers.utils.toUtf8Bytes("testpdf"));
    await cert.connect(owner).store(hash);
    await cert.connect(owner).store(hash); // should not revert
    const rec = await cert.get(hash);
    expect(rec.timestamp).to.be.gt(0);
  });
});
