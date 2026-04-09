# eCommerce Backend API (Django + DRF)

A backend-only eCommerce project designed for portfolio use and real frontend integration.
This repository focuses on clean domain logic: authentication, cart operations, checkout, order history, and payment status handling.

## Why This Project Is Strong For CV

- API-first architecture that works with any frontend stack.
- Real eCommerce flow: add to cart, validate stock, checkout, create order items, and process payment state.
- Clear modular structure using Django apps.
- Transaction-safe checkout logic to avoid partial order creation.

## Tech Stack

- Python 3
- Django 6
- Django REST Framework
- DRF Token Authentication
- SQLite for local development

## Core Business Logic

- Users and addresses: register/login and manage delivery addresses.
- Products: public browsing and search.
- Cart: add/update/delete items with stock validation and total recalculation.
- Orders: checkout converts cart items into immutable order items.
- Payments: one payment per order with pending/success/failed states.

## Project Structure

- apps/users: account, profile, address logic
- apps/products: product catalog logic
- apps/cart: cart rules and totals
- apps/orders: checkout and order history logic
- apps/payment: payment state model and actions
- eCommerce: project settings and root config

## Quick Start (CMD)

1. Clone the repository.
2. Open CMD inside the project root.
3. Install dependencies.
4. Run migrations.
5. Create an admin user.
6. Run the server.

Commands:

python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

## Authentication Flow

1. Register a user or login using username/password.
2. Receive token from backend.
3. Send token in request header for protected endpoints.

Header format:

Authorization: Token YOUR_TOKEN_HERE

## Minimal Endpoint Summary

- Auth and users: register, login, profile, address CRUD
- Products: list, detail, search
- Cart: view cart, add item, update item, remove item
- Orders: checkout, list orders, order detail
- Payments: create payment, mark success, mark failed

Full examples are in [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

## Frontend Integration Notes

- This is backend-only by design.
- Frontend sends JSON to endpoints and renders UI/errors.
- Backend serializers perform final validation.
- Checkout always revalidates stock before creating order.

## Development Notes

- Default database is SQLite for local setup.
- Payment flow uses a minimal internal status model suitable for extension to Stripe/PayPal later.
- Admin site can be used to inspect users, orders, and payments quickly.

## Documentation

- API details: [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## License

Use this project as a learning and portfolio base. Add your preferred license before public distribution.
