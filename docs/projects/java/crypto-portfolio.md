---
title: "Crypto Portfolio API"
date: 2025-01-20
categories:
  - Java
  - Spring
  - Projects
description: "A Spring Boot microservices-style API for managing cryptocurrency portfolios; integrating with CoinMarketCap via WebClient for real-time exchange rates."
reading_time: 6
---

# Crypto Portfolio API

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: &nbsp;<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/spring/"><em>Spring</em></a>&nbsp;•&nbsp;
      ⏱️ ~6 min read</span>
    </span>
  </div>
</div>

> "Built to learn, WebClient, reactive programming, and real API integration, not just theory. The kind of project you do on a job test."

---

## What Is It

The Crypto Portfolio API lets users manage portfolios of cryptocurrency holdings. Users can create multiple portfolios, add holdings to each, and get their total valuation in different currencies (USD, MAD, EUR, etc.).

The app consists of two services:

- **Portfolio Service** (port 8080) : manages users, portfolios, and holdings
- **Exchange Rate Service** (port 8081) : fetches real-time crypto prices from [CoinMarketCap](https://coinmarketcap.com/api/documentation/v1/){target="_blank"}

!!! note "Architecture Note"
    While the services run on separate ports and follow a modular structure, this is not a full microservices architecture. It's a step toward understanding service separation and inter-service communication via [WebClient](https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html){target="_blank"}.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Java 17 |
| Framework | Spring Boot 3.4.1 |
| Build | Maven |
| Database | H2 (in-memory) |
| Persistence | Hibernate / JPA |
| HTTP Client | WebClient (reactive) |
| Testing | JUnit, Mockito, WebTestClient, MockWebServer |
| External API | CoinMarketCap |

---

## Architecture

```
crypto-portfolio-api/
├── exchangerateservice/    # Fetches crypto prices from CoinMarketCap
│   └── port: 8081
└── portfolioservice/       # Manages users, portfolios, holdings
    └── port: 8080
```

The Portfolio Service calls the Exchange Rate Service via **WebClient** to fetch live prices when calculating portfolio valuations.

---

## API Endpoints

### Exchange Rate Service

```
GET /exchange-rate/latest                        # latest rates for all supported cryptos
GET /exchange-rate?symbol={symbol}&base={base}   # price for a specific crypto in a base currency
```

### Portfolio Service

```
POST   /users                                                          # create user
GET    /users/{userId}                                                 # get user
PATCH  /users/{userId}                                                 # update user
DELETE /users/{userId}                                                 # delete user
GET    /users/{userId}/portfolios/all                                  # all portfolios for a user

POST   /users/{userId}/portfolios                                      # create portfolio
GET    /users/{userId}/portfolios/{portfolioId}                        # get portfolio
PATCH  /users/{userId}/portfolios/{portfolioId}                        # update portfolio
DELETE /users/{userId}/portfolios/{portfolioId}                        # delete portfolio

POST   /users/{userId}/portfolios/{portfolioId}/holdings               # add holding
GET    /users/{userId}/portfolios/{portfolioId}/holdings/{symbol}      # get holding
PATCH  /users/{userId}/portfolios/{portfolioId}/holdings/{symbol}      # update holding
DELETE /users/{userId}/portfolios/{portfolioId}/holdings/{symbol}      # remove holding
GET    /users/{userId}/portfolios/{portfolioId}/holdings/all           # all holdings
GET    /users/{userId}/portfolios/{portfolioId}/valuation?base={base}  # portfolio value
```

---

## Running It

```bash
# Clone
git clone git@github.com:alfahami/crypto-portfolio-api.git
cd crypto-portfolio-api

# Terminal 1: Exchange Rate Service
cd exchangerateservice
mvn clean install
mvn spring-boot:run

# Terminal 2: Portfolio Service
cd portfolioservice
mvn clean install
mvn spring-boot:run
```

**Run tests:**

```bash
cd exchangerateservice && mvn test
cd portfolioservice && mvn test
```

A Postman collection is included in the repo: `crypto-portfolio.postman_collection.json`

---

## Key Challenges & Decisions

### 1. WebClient and Reactive Programming

The Exchange Rate Service uses **WebClient** instead of `RestTemplate` to call CoinMarketCap. This was the main learning objective of the project; understanding how reactive HTTP clients work, how to handle responses, and how to test them with `WebTestClient` and `MockWebServer`.

### 2. User → Portfolio → Holding Validation

When managing holdings, every operation needed to validate that the holding belongs to the right portfolio and the portfolio belongs to the right user. Three approaches were tried:

- Injecting `UserRepository` directly into `HoldingService` ; works but mixes concerns
- Injecting `PortfolioServiceImp` into `HoldingService` ; creates tight coupling
- Creating a dedicated `ValidationAuthorizationService` ; cleanest approach, respects Single Responsibility Principle

### 3. Preventing ID Tampering on Updates

When updating an entity via `PATCH`, there's a risk of ID mismatch between the URI and the request body. The solution: ignore the ID from the request body entirely, retrieve the entity using the URI ID, validate, then update and save the retrieved object.

### 4. MockWebServer Management in Tests

Used `MockWebServer` from OkHttp to simulate the Exchange Rate Service in Portfolio Service integration tests. Key practices:

- Start server once with `@BeforeAll`, shut down with `@AfterAll`
- Each test enqueues its own response for predictable behavior
- Only one test relied on the external service so no manual request clearing was needed

---

## Key Learnings

- **WebClient** : reactive HTTP client, how it differs from `RestTemplate`, and how to test it properly
- **MockWebServer** : simulating external APIs in integration tests without hitting real endpoints
- **Inter-service communication** : how two Spring Boot services talk to each other via REST
- **JPA relationships** : designing User → Portfolio → Holding entity relationships with proper cascade and validation
- **Global exception handling** : using `@ControllerAdvice` for consistent error responses across all endpoints
- **Transaction management** : ensuring atomic updates when modifying related entities

> While building this project I went deep on **WebClient and reactive programming** : a dedicated article on that is coming to the [Spring section](../../spring/index.md).

---

## Links

- [GitHub Repository](https://github.com/alfahami/crypto-portfolio){target="_blank"}
- [CoinMarketCap API Docs](https://coinmarketcap.com/api/documentation/v1/){target="_blank"}
- [WebClient](https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html){target="_blank"}.

---

## License

MIT - open source and free to use.