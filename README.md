# Expenses_Tracker_API
# 💰 Expense Tracking Management System API 🚀

---

## 1. Project Overview

The Expense Tracking Management System API is a backend service designed to help users effectively **record, categorize, and summarize their daily spending**. This system provides robust user authentication and a simple, centralized way to manage personal finances, allowing users to gain insights into where their money goes.

---

## ✨ 2. Core Features

The API supports the following functionalities:

* **User Authentication**: Secure user registration, login, and logout using **token-based authentication**.
* **Expense CRUD**: Users can **Create, Read, Update, and Delete** their own expense records.
* **Data Categorization**: Expenses are categorized using a **simple text string** (e.g., "Food", "Rent") directly on the expense record.
* **Filtering**: Users can query expenses by **Date** and the **Category String**.
* **Spending Summaries**: Endpoints provide aggregated views of total spending broken down by category for weekly or monthly periods.
* **Admin Control**: Admin users have elevated privileges, including the ability to manage all expenses and "ban" users from creating new entries.

---

## 🛠️ 3. Technology Stack

* **API Framework**: **Django REST Framework (DRF)**
* **Database**: (Placeholder: e.g., PostgreSQL or SQLite)
* **Authentication**: Token-based Authentication

---

## 💾 4. Database Schema (ERD)

The system relies on two main entities: **User** and **Expense**. The relationship between them is **One-to-Many** ($\text{1:N}$).

### 1. User Entity
The User entity manages account authentication, ownership, and permissions.

#### Attributes:
* **id**: Unique Identifier (Used for linking)
* **username**: Account login name
* **email**: Contact information
* **password**: Securely stored credential
* **is\_admin**: Role flag for administrative privileges
* **is\_banned**: Status flag controlling expense creation ability

#### Relationships
* **One User $\rightarrow$ Many Expenses**

A single **User** owns and records many expense entries, forming the basis of their financial history.

### 2. Expense Entity
The Expense entity represents a single transaction record.

#### Attributes:
* **id**: Unique Identifier (Used for tracking)
* **amount**: Value of the transaction
* **category**: Descriptive text tag for classification (e.g., "Travel," "Food")
* **description**: Optional details about the spending
* **date**: When the expense occurred
* **user\_id**: Link to the User who created the record

#### Relationships
* **One Expense $\rightarrow$ One User**

Each expense record is created by and belongs to exactly one user.

---

## 🔌 5. API Endpoints List

### Authentication & Users
| Method | Endpoint | Description | Permission |
| :--- | :--- | :--- | :--- |
| POST | `/api/register/` | Register a new user (requires username, email, password). | Public |
| POST | `/api/login/` | Log in and return an authentication token. | Public |
| POST | `/api/logout/` | Log out and invalidate the token. | Authenticated |

### Expenses CRUD
| Method | Endpoint | Description | Permission |
| :--- | :--- | :--- | :--- |
| GET | `/api/expenses/` | List all expenses for the logged-in user. | Owner Only / Admin |
| POST | `/api/expenses/` | Create a new expense (requires amount, category, description, date). | Owner Only (Must not be banned) |
| GET | `/api/expenses/<id>/` | Get details of a specific expense by ID. | Owner Only / Admin |
| PUT | `/api/expenses/<id>/` | Update an existing expense by ID. | Owner Only |
| DELETE | `/api/expenses/<id>/` | Delete an expense by ID. | Owner Only / Admin |

### Filtering & Summaries
| Method | Endpoint | Description | Permission |
| :--- | :--- | :--- | :--- |
| GET | `/api/expenses/category/<category>/` | Filter expenses by the **category string** stored on the record. | Owner Only |
| GET | `/api/expenses/date/<yyyy-mm-dd>/` | Filter expenses by a specific date. | Owner Only |
| GET | `/api/expenses/summary/monthly/` | View total spending and breakdown summary for the current month. | Owner Only |
| GET | `/api/expenses/summary/weekly/` | View total spending and breakdown summary for the current week. | Owner Only |