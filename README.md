# 📦 Blockchain Yuka - Inventory & Transaction API

RESTful API for product and transaction management with JWT authentication, user permissions, and blockchain (hash) logging.

---

## 🔐 Authentication

All protected endpoints require a JWT token in the header:

```
Authorization: Bearer <your_token>
```

---

## 🚀 Endpoints

### 🧑‍💼 Auth

**POST /login**  
Authenticates a user and returns a JWT.

**Request:**
```json
{
  "email": "admin@email.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "..."
}
```

---

### 👤 Users

**POST /users** (admin only)  
Creates a new user.

**GET /users**  
Lists all users.

**GET /users/<id>**  
Returns user data.

**PUT /users/<id>**  
Updates user data.

**DELETE /users/<id>**  
Removes a user.

---

### 📦 Products

**POST /product** (admin only)  
Creates a product.

**GET /product**  
Lists all products.

**GET /product/<id>**  
Returns a product.

**PUT /product/<id>**  
Updates a product.

**DELETE /product/<id>**  
Removes a product.

---

### 🔄 Transactions

**POST /entry**  
Registers product entry.

**POST /exit**  
Registers product exit.

**GET /transactions**  
Lists all transactions.

**GET /transactions/<id>**  
Returns a specific transaction.

**GET /transactions/by-product/<product_id>**  
Lists transactions of a product.

**GET /user/transactions**  
Lists transactions made by the logged-in user.

**DELETE /transactions/<id>**  
Removes a transaction.

---

## ⚙️ Permissions

- **ADMIN:** Full Access
- **OPERATOR:** Registers Entries and Exits
- **VIEWER:** Read-Only Access

---

## 📌 Notes

- Transactions generate a `blockchain_hash` SHA-256 to simulate immutability.
- Inventory is automatically updated when registering entries and exits.
