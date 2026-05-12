---
title: "BCertificate"
date: 2021-01-01
categories:
  - Blockchain
  - Projects
description: "A Hyperledger Fabric blockchain network that automates the issuance, dispatch, and management of university digital credentials; diplomas, transcripts, and degree certifications."
reading_time: 5
---

# BCertificate

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: &nbsp;<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/blockchain/"><em>Blockchain</em></a>&nbsp;•&nbsp;
      ⏱️ ~5 min read</span>
    </span>
  </div>
</div>

> "A blockchain network that lets schools and universities add credentials to an immutable ledger; making diploma fraud a thing of the past."

---

## What Is It

BCertificate is a full blockchain application built on **Hyperledger Fabric v2.x** that automates the issuance, dispatch, and management of university digital credentials; diplomas, skills assessments, transcripts, and degree certifications.

The core idea: universities write credentials to a distributed ledger. Employers and institutions can verify them without contacting the university directly. No more fake diplomas, no more verification delays.

This was my first Hyperledger Fabric project, built to get hands-on with enterprise blockchain before extending the concept to land certificate management in [landcertificate](landcertificate.md).

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

---

## How It Works

The network consists of organizations (universities) that each run their own peers. A shared channel connects them, and the chaincode (smart contract) runs on all peers.

**Flow:**

1. Admin enrolls and registers a user against the Certificate Authority
2. University submits a credential transaction; the chaincode validates and writes it to the ledger
3. Anyone with network access can query a certificate by ID
4. Bulk import via Excel sheet is supported for adding multiple credentials at once

**Key chaincode operations:**

- `initLedger` — seeds the ledger with initial certificates on deploy
- `addCertificate` — writes a new credential to the blockchain
- `queryCertificate` — retrieves a credential by ID
- `queryAllCertificates` — returns all credentials in the ledger

---

## Project Structure

```
bcertificate/
├── certificate-network/
│   ├── chaincode/certificate/   # Smart contract (JS and Java)
│   ├── certificate-starter/
│   │   ├── startBCertificate.sh # Starts the full network
│   │   ├── networkDown.sh       # Tears down the network
│   │   ├── javascript/          # Admin enroll, user register, query scripts
│   │   ├── java/                # Java admin scripts
│   │   └── apiserver/           # Node.js REST API + web app
└── screenshots/
```

---

## Running It

Prerequisites: Docker installed and configured. Hyperledger Fabric binaries set up.

```bash
# Start the network, deploy chaincode, initialize ledger
./startBCertificate.sh

# Enroll admin, register user, query initial data
cd apiserver/
node enrollAdmin.js && node registerUser.js && node query.js

# Start the API server
node apiserver.js
```

Then visit:

- `http://localhost:8080/api/allcertificates` — all credentials in the ledger
- `http://localhost:8080/api/addcertificate` — add a new credential
- `http://localhost:8080/api/query/CERT11` — query a specific certificate

---

## Key Learnings

- **Hyperledger Fabric architecture** — understanding organizations, peers, orderers, channels, and the Certificate Authority
- **Chaincode lifecycle** — packaging, installing, approving, and committing chaincode across organizations
- **Fabric SDK** — enrolling admins, registering users, and submitting transactions from a Node.js client
- **Docker networking** — how Fabric spins up containers for each peer and orderer
- **Permissioned vs public blockchain** — why enterprise use cases need identity and access control that public chains like Ethereum don't provide

---

## Links

- [:fontawesome-brands-github: GitHub Repository](https://github.com/alfahami/bcertificate)
- [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/)
- [Related project: landcertificate](landcertificate.md)