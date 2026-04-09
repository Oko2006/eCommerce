# API Documentation

Base URL for local development:
http://127.0.0.1:8000

Authentication for protected routes:
Authorization: Token YOUR_TOKEN_HERE

## 1. Auth and Users

### Register

POST /api/users/register/

Request JSON:
{
"username": "omar",
"email": "omar@example.com",
"password": "StrongPass123",
"first_name": "Omar",
"last_name": "Alomari",
"phone_number": "0790000000"
}

Response:

- token
- user object

### Login

POST /api/users/login/

Request JSON:
{
"username": "omar",
"password": "StrongPass123"
}

Response:

- token
- user object

### Profile

GET /api/users/profile/

Response:

- current authenticated user object

### Address CRUD

GET /api/users/addresses/
POST /api/users/addresses/
GET /api/users/addresses/{id}/
PATCH /api/users/addresses/{id}/
DELETE /api/users/addresses/{id}/

Address JSON:
{
"street": "36 St",
"city": "zarqa",
"state": "Zarqa",
"postal_code": "00001",
"country": "Jordan"
}

## 2. Products

### List Products

GET /api/products/

### Search Products

GET /api/products/?q=keyboard

### Product Detail

GET /api/products/{id}/

## 3. Cart

### Get My Cart

GET /api/cart/

### Add Item

POST /api/cart/items/

Request JSON:
{
"product_id": 1,
"quantity": 2
}

Notes:

- If product already exists in cart, quantity is increased.
- Backend checks stock before adding.

### Update Item Quantity

PATCH /api/cart/items/{item_id}/

Request JSON:
{
"quantity": 3
}

### Delete Item

DELETE /api/cart/items/{item_id}/

## 4. Orders

### Checkout

POST /api/orders/checkout/

Request JSON:
{
"address_id": 1
}

What happens internally:

- validates address belongs to user
- validates cart is not empty
- validates stock for each item
- creates Order
- creates OrderItem records
- decreases product stock
- clears cart

### List Orders

GET /api/orders/

### Order Detail

GET /api/orders/{id}/

## 5. Payments

### Create Payment

POST /api/payments/

Request JSON:
{
"order": 1,
"provider": "cod"
}

Notes:

- one payment per order
- payment amount is copied from order total

### Mark Payment Success

PATCH /api/payments/{id}/mark_success/

Optional JSON:
{
"transaction_id": "txn_123"
}

### Mark Payment Failed

PATCH /api/payments/{id}/mark_failed/

Optional JSON:
{
"transaction_id": "txn_failed_123"
}

## Common Error Cases

- 400: invalid payload, stock issues, duplicate payment
- 401: missing or invalid token
- 404: resource not found or not owned by current user

## Suggested Testing Order

1. Register user
2. Login and copy token
3. Create address
4. Create product from admin
5. Add product to cart
6. Checkout
7. Create payment
8. Mark payment success
