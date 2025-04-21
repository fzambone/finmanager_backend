# FinManage Backend API

## Description

This project provides the backend API service for FinManage, a personal finance management web application. It allows users to manage financial accounts, track transactions, categorize spending/income, and (in future versions) manage budgets, all within the context of a Family Group. The API uses Django and Django REST Framework, with JWT for authentication.

**Phase 1 Goal:** Provide core API functionality for managing personal/family finances, focusing initially on Accounts, Categories, and Transactions with user authentication and data isolation between Family Groups.

## Tech Stack

* **Backend Framework:** Django
* **API Framework:** Django REST Framework (DRF)
* **Authentication:** `dj-rest-auth` with `djangorestframework-simplejwt` (JWT Tokens, Email/Password Login) and `django-allauth` (for underlying account management).
* **Database:** SQLite (for development), PostgreSQL (intended for production)
* **Core Language:** Python

## Project Structure

The project follows a multi-app structure for modularity:

* `finmanage_project/`: Main Django project settings and configuration.
* `core/`: Shared utilities, base models (e.g., `SoftDeleteModel`), custom serializers (e.g., `CustomRegisterSerializer`).
* `groups/`: Manages `FamilyGroup` model and membership.
* `accounts/`: Manages financial `Account` models and related logic.
* `categories/`: Manages `Category` models (including sub-categories).
* `transactions/`: Manages `Transaction` models.
* *(Future apps like `budgets`, `reports` may be added)*

## Local Development Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd finmanage_backend
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv .venv
    # Windows (Git Bash/PowerShell)
    source .venv/Scripts/activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create Superuser (for Admin Access):**
    ```bash
    python manage.py createsuperuser
    # Follow prompts (enter username, email, password)
    ```
6.  **Run Development Server:**
    ```bash
    python manage.py runserver
    ```
    The API should be accessible at `http://127.0.0.1:8000/`. The Django Admin is at `http://127.0.0.1:8000/admin/`.

## Key Concepts

* **Authentication:** Uses JWT (JSON Web Tokens). Clients must first register, then log in via the `/api/v1/auth/login/` endpoint to receive an `access_token` and `refresh_token`. The `access_token` must be included in the `Authorization: Bearer <token>` header for subsequent requests to protected endpoints. Email is used for login.
* **Family Groups:** All core financial data (Accounts, Categories, Transactions) is scoped to a `FamilyGroup`. Users belong to one group. API endpoints automatically filter data based on the authenticated user's group membership. Currently, groups and memberships are managed via the Django Admin (`/admin/groups/familygroup/`).
* **Soft Delete:** Core models (`Account`, `Category`, `Transaction`, `FamilyGroup`) use a soft-delete pattern. Items are marked with a `deleted_at` timestamp instead of being removed from the database. Standard API views exclude soft-deleted items.

## API Endpoint Summary

All API endpoints are prefixed with `/api/v1/`. Authentication (Bearer Token) is required unless otherwise noted.

**Authentication (`/api/v1/auth/`)**

* `POST /api/v1/auth/registration/`
    * **Auth:** None required.
    * **Request Body:** `{ "email": "...", "password": "...", "password2": "..." }`
    * **Response:** `201 Created` with user details (e.g., email, pk) on success. Errors on duplicate email or mismatched passwords.
* `POST /api/v1/auth/login/`
    * **Auth:** None required.
    * **Request Body:** `{ "email": "...", "password": "..." }`
    * **Response:** `200 OK` with `{ "access_token": "...", "refresh_token": "...", "user": {...} }` on success.
* `POST /api/v1/auth/logout/`
    * **Auth:** Bearer Token required.
    * **Request Body:** Empty.
    * **Response:** `200 OK` with detail message (client must discard token).
* `GET /api/v1/auth/user/`
    * **Auth:** Bearer Token required.
    * **Response:** `200 OK` with details of the authenticated user (`{ "pk": ..., "email": ... }`).

**Accounts (`/api/v1/accounts/`)**

* `GET /api/v1/accounts/`
    * **Auth:** Required.
    * **Response:** `200 OK` with a list of accounts belonging to the user's group.
* `POST /api/v1/accounts/`
    * **Auth:** Required.
    * **Request Body:** `{ "name": "...", "account_type": "CHECKING" | "SAVINGS" | ..., "currency": "USD" | "BRL" | ..., "starting_balance": "100.00" }` (*Do not send `family_group`*).
    * **Response:** `201 Created` with the new account details. `family_group` is assigned automatically.
* `GET /api/v1/accounts/{id}/`
    * **Auth:** Required.
    * **Response:** `200 OK` with details of the specified account (if in user's group), `404 Not Found` otherwise.
* `PUT /api/v1/accounts/{id}/` (Full Update) / `PATCH /api/v1/accounts/{id}/` (Partial Update)
    * **Auth:** Required.
    * **Request Body:** `{ "name": "...", ... }` (*Do not send `family_group`*).
    * **Response:** `200 OK` with updated account details (if in user's group), `404 Not Found` otherwise.
* `DELETE /api/v1/accounts/{id}/`
    * **Auth:** Required.
    * **Response:** `204 No Content` on successful soft delete (if in user's group), `404 Not Found` otherwise.

**Categories (`/api/v1/categories/`)**

* `GET /api/v1/categories/`
    * **Auth:** Required.
    * **Response:** `200 OK` with a list of categories belonging to the user's group (includes nested `parent_category` and `sub_categories` with id/name).
* `POST /api/v1/categories/`
    * **Auth:** Required.
    * **Request Body:** `{ "name": "...", "parent_category_id": <parent_id_or_null> }` (*Do not send `family_group`*).
    * **Response:** `201 Created`. `family_group` assigned automatically. `parent_category_id` must be null or a valid category ID *within the user's group*.
* `GET /api/v1/categories/{id}/`
    * **Auth:** Required.
    * **Response:** `200 OK` with details (including nested parent/subs) (if in user's group), `404 Not Found` otherwise.
* `PUT /api/v1/categories/{id}/` / `PATCH /api/v1/categories/{id}/`
    * **Auth:** Required.
    * **Request Body:** `{ "name": "...", "parent_category_id": <id_or_null> }` (*Do not send `family_group`*).
    * **Response:** `200 OK` (if in user's group), `404 Not Found` otherwise.
* `DELETE /api/v1/categories/{id}/`
    * **Auth:** Required.
    * **Response:** `204 No Content` on successful soft delete (if in user's group), `404 Not Found` otherwise.

**Transactions (`/api/v1/transactions/`)**

* `GET /api/v1/transactions/`
    * **Auth:** Required.
    * **Response:** `200 OK` with a list of transactions belonging to the user's group.
* `POST /api/v1/transactions/`
    * **Auth:** Required.
    * **Request Body:** `{ "transaction_type": "INCOME" | "EXPENSE" | "TRANSFER", "amount": "50.00", "date_time": "YYYY-MM-DDTHH:MM:SSZ", "account": <account_id>, "category": <category_id_or_null>, "payee_payer": "...", "description": "...", "is_recurring": false }` (*Do not send `family_group`*).
    * **Response:** `201 Created`. `family_group` assigned automatically. `account` and `category` IDs must belong to the user's group.
* `GET /api/v1/transactions/{id}/`
    * **Auth:** Required.
    * **Response:** `200 OK` (if in user's group), `404 Not Found` otherwise.
* `PUT /api/v1/transactions/{id}/` / `PATCH /api/v1/transactions/{id}/`
    * **Auth:** Required.
    * **Request Body:** `{ ... fields to update ... }` (*Do not send `family_group`*). `account`/`category` IDs must be valid for the group.
    * **Response:** `200 OK` (if in user's group), `404 Not Found` otherwise.
* `DELETE /api/v1/transactions/{id}/`
    * **Auth:** Required.
    * **Response:** `204 No Content` on successful soft delete (if in user's group), `404 Not Found` otherwise.

## Testing with API Client (e.g., Postman)

1.  Use the Registration endpoint to create a user.
2.  Use the Login endpoint with the user's email/password to get JWT tokens.
3.  Copy the `access_token`.
4.  For protected requests, add an `Authorization` header with the value `Bearer <your_access_token>`.
5.  (Recommended) Configure Postman Environments and Test Scripts to automate token handling (see Postman docs).
6.  Use the Django Admin (`/admin/`) to create a `FamilyGroup` and add your registered user to its `members` list before creating accounts/categories/transactions via the API.

