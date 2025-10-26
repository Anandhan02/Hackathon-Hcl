# SmartBank - Modular Banking Backend System

SmartBank is a full-stack digital banking platform built with **FastAPI (Python)** on the backend and **React (Vite + Redux)** on the frontend.  
It provides secure, scalable, and modular banking operations including **user management**, **account creation**, **transactions**, **reporting**, and **role-based access control** — powered by **GraphQL APIs** and **MongoDB**.



## Architecture Overview

SmartBank follows a modular, service-oriented architecture with clear separation between frontend, backend, and database layers.

## Tech Stack

**Frontend**
- React (JavaScript)
- Vite
- TailwindCSS
- Redux Toolkit
- React Router

**Backend**
- FastAPI (Python)
- Strawberry GraphQL
- Motor (Async MongoDB driver)
- JWT Authentication


**Database**
- MongoDB (NoSQL)

**Other Tools**

- Pytest (testing)
- SlowAPI (rate limiting)

---

## Features

### User Management
- Register and log in with JWT authentication.
- Password hashing using bcrypt.
- Role-based access: Customer, Admin, Auditor.

### Account Management
- Create and view multiple accounts.
- Supports Savings, Current, and Fixed Deposit types.
- Auto-generates unique 10-digit account numbers.

### Transactions
- Deposit, withdraw, and transfer funds.
- Atomic balance updates with MongoDB transactions.
- Daily transaction limits and validation.
- Detailed transaction history.

### Role-Based Access Control (RBAC)
- Customers manage personal accounts.
- Admins manage all users and accounts.
- Auditors have read-only access to audit logs.

### Reporting & Dashboard
- GraphQL queries for account summaries and statistics.
- Admin dashboard for user and transaction insights.

### Security
- JWT-based authentication.
- Password hashing with bcrypt.
- Input validation using Pydantic.
- Rate limiting (SlowAPI).
- CORS protection.
- Environment-based configuration.

---

## GraphQL API Overview

All operations are accessible via a single endpoint:

**Endpoint:** `/graphql`

---

### Queries

| Query | Description |
|--------|-------------|
| `me` | Fetch the current authenticated user. |
| `accounts` | Retrieve all accounts owned by the logged-in user. |
| `account(accountId: ID!)` | Get account details and transactions. |
| `transactions(accountId: ID!, limit: Int)` | Retrieve recent transactions. |
| `users` *(Admin only)* | List all registered users. |
| `reports` *(Admin only)* | Fetch admin system summaries. |

---

### Mutations

| Mutation | Description |
|-----------|-------------|
| `registerUser(name, email, password)` | Register a new user and return a JWT. |
| `loginUser(email, password)` | Authenticate credentials and return tokens. |
| `createAccount(accountType, initialDeposit)` | Create a new account for a user. |
| `deposit(accountId, amount)` | Deposit funds into an account. |
| `withdraw(accountId, amount)` | Withdraw funds (if balance is sufficient). |
| `transfer(fromAccountId, toAccountNumber, amount)` | Transfer funds securely between accounts. |
| `toggleAdmin(userId)` *(Admin only)* | Toggle admin privileges for a user. |

---



## MongoDB Collections

---

### **users**

| Field | Type | Description |
|--------|------|-------------|
| `_id` | ObjectId | Primary key |
| `name` | String | Full name |
| `email` | String | Unique email |
| `password_hash` | String | Hashed password |
| `roles` | [String] | User roles (Customer/Admin/Auditor) |
| `created_at` | Date | Account creation timestamp |

---

### **accounts**

| Field | Type | Description |
|--------|------|-------------|
| `_id` | ObjectId | Primary key |
| `user_id` | ObjectId | Reference to user |
| `account_number` | String | Unique 10-digit account number |
| `account_type` | String | "savings", "current", or "fd" |
| `balance` | Decimal | Current balance |
| `daily_limit` | Decimal | Daily transfer limit |
| `created_at` | Date | Timestamp |

---

### **transactions**

| Field | Type | Description |
|--------|------|-------------|
| `_id` | ObjectId | Primary key |
| `account_id` | ObjectId | Source account |
| `counterparty_account_id` | ObjectId | Destination account |
| `amount` | Decimal | Transaction amount |
| `type` | String | "deposit", "withdraw", or "transfer" |
| `status` | String | "pending", "posted", or "failed" |
| `created_at` | Date | Timestamp |
| `idempotency_key` | String | Prevents duplicate transfers |

---

### **audit_logs**

| Field | Type | Description |
|--------|------|-------------|
| `_id` | ObjectId | Primary key |
| `user_id` | ObjectId | Actor performing the action |
| `action` | String | Operation performed |
| `resource` | String | Entity affected (account, transaction, etc.) |
| `timestamp` | Date | Operation timestamp |
| `ip` | String | IP address of requester |
## GraphQL Operations

---


## *Graphql*

```graphql
## Login
mutation {
  loginUser(email: "alice@bank.com", password: "Secure123") {
    accessToken
    user {
      id
      name
    }
  }
}

## Create Account
mutation {
  createAccount(accountType: "savings", initialDeposit: 5000.0) {
    id
    accountNumber
    balance
  }
}


## Fetch Accounts
query {
  accounts {
    id
    accountNumber
    accountType
    balance
  }
}
