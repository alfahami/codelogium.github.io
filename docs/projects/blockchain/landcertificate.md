---
title: "LandCertificate"
date: 2023-06-26
categories:
  - Blockchain
  - Projects
description: "A Hyperledger Fabric blockchain application where clients request land certificates from a land conserver (admin) who certifies ownership on the blockchain; with QR code verification and MongoDB Atlas for request storage."
reading_time: 6
---

# LandCertificate

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: &nbsp;<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/blockchain/"><em>Blockchain</em></a>&nbsp;•&nbsp;
      ⏱️ ~6 min read</span>
    </span>
  </div>
</div>

> "A blockchain network that lets land conservers certify land ownership on an immutable ledger; helping against land ownership fraud and disputes."

---

## What Is It

LandCertificate is a Hyperledger Fabric blockchain application with a **dual-role system**; clients request land certificates from a land conserver (admin) who validates and certifies ownership on the blockchain. Each certified land gets a **QR code** for easy verification.

It's the evolution of [bcertificate](bcertificate.md), same Hyperledger Fabric foundation, but with a real client/admin workflow, QR code generation, and MongoDB Atlas for persisting client requests.

Built on **Hyperledger Fabric v2.x**, tested on Linux/Debian 10 Buster, WSL/Debian 10 Buster, and WSL/Ubuntu.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Blockchain | Hyperledger Fabric v2.x |
| Smart Contract | JavaScript / Java (Chaincode) |
| Backend | Node.js, Express.js, REST API |
| Frontend | Pug template engine, CSS |
| Database | MongoDB Atlas (client requests) |
| Infrastructure | Docker |
| Extra | QR Code generation |

---

## How It Works

The system has two distinct user roles:

**Client:**

1. Visits the client portal and fills a land certificate request form
2. Request is stored in MongoDB Atlas
3. Admin receives the request in their panel

**Admin (Land Conserver):**

1. Reviews incoming requests in the admin panel
2. Validates and adds the land certificate to the blockchain
3. Certificate is written to the Hyperledger Fabric ledger with a QR code generated for verification

**Key chaincode operations:**

- `initLedger`: seeds the ledger with initial land certificates on deploy
- `addLandCertificate`: writes a certified land to the blockchain
- `queryLandCertificate`: retrieves a land certificate by ID
- `queryAllLandCertificates`: returns all certified lands in the ledger

---

## Project Structure

```
landcertificate/
├── landcertificate-network/
│   ├── chaincode/landcertificate/  # Smart contract (JS and Java)
│   └── landcertificate-starter/
│       ├── startBcLand.sh          # Starts the full network
│       ├── networkDown.sh          # Tears down the network
│       ├── javascript/             # Admin enroll, user register, query scripts
│       ├── java/                   # Java admin scripts (partial)
│       └── apiserver/              # Node.js REST API + web app
└── screenshots/
```

---

## Running It

!!! note "TL;DR"
    If you're already familiar with Hyperledger Fabric and have everything set up, go directly to `landcertificate-network/landcertificate-starter/` and run the commands below.

**Prerequisites:**

- Docker installed and configured
- Hyperledger Fabric binaries set up ([official docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/install.html))

**Install Hyperledger Fabric:**

```bash
curl -sSL https://bit.ly/2ysbOFE | bash -s
```

**Start the network:**

```bash
# From landcertificate-network/landcertificate-starter/
./startBcLand.sh

# Enroll admin, register user, query initial data
cd apiserver/
node enrollAdmin.js && node registerUser.js && node query.js

# Start the API server
node apiserver.js
```

Then visit:

- `http://localhost:8080/api/admin/index`: admin panel with all certified lands
- `http://localhost:8080/api/admin/addland`: add a new land certificate
- `http://localhost:8080/client/index`: client request portal

---

## Screenshots

**Admin panel: all certified lands:**

![Admin all certificates](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/admin_all_certificates.png)

**Admin: adding a new land certificate:**

![Admin add land](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/admin_addland.png)

**Client: request form:**

![Client index](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/client_index.png)

**Client: form filled:**

![Client form filled](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/client_req_filled.png)

**Client: form submitted:**

![Client request sent](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/client_req_sent.png)

**Admin receives the request:**

![Admin add land filled](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/admin_addland_filled.png)

**All certified lands after validation:**

![Admin all certificates updated](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/admin_all_certificates_w_newly_entered.png)

**Certified land with QR Code:**

![Land detail with QR](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/land_detail1.png)

![Land detail QR close up](https://raw.githubusercontent.com/alfahami/landcertificate/main/screenshots/land_detail2.png)

---

## Key Learnings

- **Client/Admin role separation**: designing a real-world workflow where two different actors interact with the same blockchain network
- **MongoDB Atlas integration**: combining a traditional database with blockchain; off-chain storage for requests, on-chain storage for certified data
- **QR Code generation**: embedding verification codes directly into blockchain certificates
- **Hyperledger Fabric v2.x chaincode lifecycle**: building on top of the bcertificate experience with a more complete application
- **Dual-interface web app**: separate client and admin portals backed by the same Node.js API

---

## Links

- [GitHub Repository](https://github.com/alfahami/landcertificate)
- [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/)
- [Related project: bcertificate](bcertificate.md)

---

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/)