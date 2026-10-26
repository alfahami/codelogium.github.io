---
title: "LandCertificate"
date: 2023-06-26
categories:
  - Blockchain
  - Projects
description: "A Hyperledger Fabric blockchain application where clients request land certificates from a land conserver (admin) who certifies ownership on the blockchain; with QR code verification and MongoDB Atlas for request storage."
reading_time: 6
repo: https://github.com/alfahami/landcertificate
stack:
  - Hyperledger Fabric
  - Node.js
  - Express.js
  - Pug
  - MongoDB Atlas
  - Docker
icon: lucide/map
tags:
  - Blockchain
---

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
- Hyperledger Fabric binaries set up ([official docs](https://hyperledger-fabric.readthedocs.io/en/release-2.2/install.html){target="_blank"})

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

![Admin all certificates](/assets/projects/landcertificate/admin_all_certificates.webp){ width="1747" height="463" loading=lazy }

**Admin: adding a new land certificate:**

![Admin add land](/assets/projects/landcertificate/admin_addland.webp){ width="1402" height="883" loading=lazy }

**Client: request form:**

![Client index](/assets/projects/landcertificate/client_index.webp){ width="1257" height="814" loading=lazy }

**Client: form filled:**

![Client form filled](/assets/projects/landcertificate/client_req_filled.webp){ width="1296" height="829" loading=lazy }

**Client: form submitted:**

![Client request sent](/assets/projects/landcertificate/client_req_sent.webp){ width="1252" height="829" loading=lazy }

**Admin receives the request:**

![Admin add land filled](/assets/projects/landcertificate/admin_addland_filled.webp){ width="1434" height="883" loading=lazy }

**All certified lands after validation:**

![Admin all certificates updated](/assets/projects/landcertificate/admin_all_certificates_w_newly_entered.webp){ width="1747" height="514" loading=lazy }

**Certified land with QR Code:**

![Land detail with QR](/assets/projects/landcertificate/land_detail1.webp){ width="1309" height="943" loading=lazy }

![Land detail QR close up](/assets/projects/landcertificate/land_detail2.webp){ width="1285" height="879" loading=lazy }

---

## Key Learnings

- **Client/Admin role separation**: designing a real-world workflow where two different actors interact with the same blockchain network
- **MongoDB Atlas integration**: combining a traditional database with blockchain; off-chain storage for requests, on-chain storage for certified data
- **QR Code generation**: embedding verification codes directly into blockchain certificates
- **Hyperledger Fabric v2.x chaincode lifecycle**: building on top of the bcertificate experience with a more complete application
- **Dual-interface web app**: separate client and admin portals backed by the same Node.js API

---

## Links

- <a href="https://github.com/alfahami/landcertificate" target="_blank">GitHub Repository</a>
- <a href="https://hyperledger-fabric.readthedocs.io/en/release-2.2/" target="_blank">Hyperledger Fabric Docs</a>
- [Related project: bcertificate](bcertificate.md)

---

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0/){target="_blank"}