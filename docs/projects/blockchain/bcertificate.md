---
title: "BCertificate"
date: 2021-12-03
categories:
  - Blockchain
  - Projects
description: "A Hyperledger Fabric blockchain network that automates the issuance, dispatch, and management of university digital credentials; diplomas, transcripts, and degree certifications."
reading_time: 6
---

# BCertificate

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: &nbsp;<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/blockchain/"><em>Blockchain</em></a>&nbsp;•&nbsp;
      ⏱️ ~6 min read</span>
    </span>
  </div>
</div>

> "A blockchain network that lets schools and universities add credentials to an immutable ledger; making diploma fraud a thing of the past."

---

## What Is It

BCertificate is a full blockchain application built on **Hyperledger Fabric v2.x** that automates the issuance, dispatch, and management of university digital credentials; diplomas, skills assessments, transcripts, and degree certifications.

The core idea: universities write credentials to a distributed ledger. Employers and institutions can verify them without contacting the university directly. No more fake diplomas, no more verification delays.

This was my first Hyperledger Fabric project, built at the Faculty of Science in Kenitra as part of my Mathematics and Computer Science studies. The main focus was getting familiar with how Hyperledger Fabric builds and handles blockchain rather than polishing the user experience.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Blockchain | Hyperledger Fabric v2.x |
| Smart Contract | JavaScript / Java (Chaincode) |
| Backend | Node.js, Express.js, REST API |
| Frontend | Pug template engine, CSS |
| Infrastructure | Docker |
| SDK | Fabric SDK Node, Fabric Java SDK |

Tested on Linux/Debian 10 Buster, WSL/Debian 10 Buster, and WSL/Ubuntu.

---

## How It Works

The network consists of organizations (universities) that each run their own peers. A shared channel connects them, and the chaincode (smart contract) runs across all peers.

**Flow:**

1. Admin enrolls and registers a user against the Certificate Authority
2. University submits a credential transaction; the chaincode validates and writes it to the ledger
3. Anyone with network access can query a certificate by ID
4. Bulk import via Excel sheet (.xls) is supported for adding multiple credentials at once

**Key chaincode operations:**

- `initLedger`: seeds the ledger with initial certificates on deploy
- `addCertificate`: writes a new credential to the blockchain
- `queryCertificate` : retrieves a credential by ID
- `queryAllCertificates`: returns all credentials in the ledger

---

## Project Structure

```
bcertificate/
├── certificate-network/
│   ├── chaincode/certificate/      # Smart contract (JS and Java)
│   └── certificate-starter/
│       ├── startBCertificate.sh    # Starts the full network
│       ├── networkDown.sh          # Tears down the network
│       ├── javascript/             # Admin enroll, user register, query scripts
│       ├── java/                   # Java admin scripts (partial)
│       └── apiserver/              # Node.js REST API + web app
└── screenshots/
```

---

## Running It

!!! note "TL;DR"
    If you're already familiar with Hyperledger Fabric and have everything set up, go directly to `certificate-network/certificate-starter/` and run the commands below.

**Prerequisites:**

- Docker installed and configured
- Hyperledger Fabric binaries set up ([official docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/install.html)){target="_blank"}
- curl installed

**Install Hyperledger Fabric:**

```bash
curl -sSL https://bit.ly/2ysbOFE | bash -s
```

If the above link doesn't work, download [fabric-samples v2.0.0](https://github.com/hyperledger/fabric-samples/releases/tag/v2.0.0-beta){target="_blank"} directly.

**Start the network:**

```bash
# From certificate-network/certificate-starter/
./startBCertificate.sh

# Enroll admin, register user, query initial data
cd apiserver/
node enrollAdmin.js && node registerUser.js && node query.js

# Start the API server
node apiserver.js
```

Then visit:

- `http://localhost:8080/api/allcertificates`: all credentials in the ledger
- `http://localhost:8080/api/addcertificate`: add a new credential
- `http://localhost:8080/api/query/CERT11`: query a specific certificate

---

## Screenshots

**All certificates in the ledger:**

![All certificates](https://raw.githubusercontent.com/alfahami/bcertificate/main/screenshots/allcertificates.png)

**Adding a certificate (with Excel bulk import support):**

![Add certificate](https://raw.githubusercontent.com/alfahami/bcertificate/main/screenshots/add-certificate.png)

**Querying a specific certificate:**

![Certificate details](https://raw.githubusercontent.com/alfahami/bcertificate/main/screenshots/git-github.png)

---

## Key Learnings

- **Hyperledger Fabric architecture**: understanding organizations, peers, orderers, channels, and the Certificate Authority
- **Chaincode lifecycle**: packaging, installing, approving, and committing chaincode across organizations
- **Fabric SDK**: enrolling admins, registering users, and submitting transactions from a Node.js client
- **Docker networking**: how Fabric spins up containers for each peer and orderer
- **Permissioned vs public blockchain**: why enterprise use cases need identity and access control that public chains like Ethereum don't provide

---

## Links

- <a href="https://github.com/alfahami/bcertificate" target="_blank">GitHub Repository</a>
- <a href="https://hyperledger-fabric.readthedocs.io/en/release-2.2/" target="_blank">Hyperledger Fabric Docs</a>

- [Related project: landcertificate](landcertificate.md)

---

## License

MIT - open source and free to use.