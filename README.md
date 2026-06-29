# 🏔️ Lakehouse Maintenance Copilot

An AI-powered Lakehouse Maintenance Copilot that monitors Apache Iceberg table health, detects lakehouse degradation, and performs controlled maintenance using an AI assistant.

---

# Project Overview

This project simulates a real-world retail company's data platform.

A PostgreSQL OLTP database acts as the operational system where customers place orders.

Apache Spark incrementally ingests this transactional data into Apache Iceberg tables, forming a lakehouse.

Over time, many small ingestion batches intentionally create the **small-file problem**. An AI Copilot monitors lakehouse health, reports degradation, and executes maintenance only after explicit user confirmation.

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## Data Engineering

- Apache Spark
- Apache Iceberg

## AI

- Claude Agent SDK
- Anthropic API

## Frontend

- Next.js
- React
- Tailwind CSS

---

# Project Structure

```text
lakehouse-maintenance-copilot/

├── backend/
│   ├── generators/
│   ├── spark/
│   ├── app/
│   └── requirements.txt
│
├── frontend/
│
├── docs/
│
└── README.md
```

---

# Phase 1 — PostgreSQL Source System ✅

The first phase builds a realistic retail OLTP database.

## Database Schema

Dimension Tables

- Categories
- Brands
- Stores
- Customers
- Products

Fact Tables

- Orders
- Order Items

The schema is normalized using foreign key relationships to mimic a production transactional database.

---

# Data Generation Process

Instead of manually inserting rows, the entire dataset is generated automatically using Python and Faker.

## Step 1

Seed master data.

Tables populated:

- Categories
- Brands
- Stores

These tables are relatively static and rarely change.

---

## Step 2

Generate Products.

Each product contains:

- Product Name
- Category
- Brand
- Price
- Stock Quantity
- Supplier
- Created Date
- Updated Date

50 products are generated.

---

## Step 3

Generate Customers.

Each customer includes:

- Name
- Email
- Phone Number
- City
- Country
- Customer Segment
- Created Date

100 customers are generated.

---

## Step 4

Generate Orders.

For every order:

- Select a random customer.
- Select a random store.
- Generate an order date.
- Select a payment method.
- Assign an order status.
- Generate between 1 and 5 unique products.

---

## Step 5

Generate Order Items.

Each order item includes:

- Product
- Quantity
- Unit Price
- Discount
- Line Total

The order total is calculated as:

```
Order Total = SUM(Line Totals)
```

ensuring referential and financial consistency.

---

# Generated Dataset

| Table | Records |
|--------|---------:|
| Categories | 10 |
| Brands | 12 |
| Stores | 8 |
| Products | 50 |
| Customers | 100 |
| Orders | 500 |
| Order Items | ~1500 |

---

# Running the Data Generator

Create the backend environment.

```bash
cd backend

python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=lakehouse_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

ANTHROPIC_API_KEY=your_api_key
```

Generate the dataset.

```bash
python generators/generate_dataset.py
```

---

# Current Progress

## ✅ Completed

- PostgreSQL database design
- Normalized schema
- SQLAlchemy connection
- Master data generator
- Product generator
- Customer generator
- Order generator
- Repository layer
- Configuration management
- Frontend Design

---

## 🚧 In Progress

- Apache Spark setup
- Apache Iceberg setup
- Initial ETL
- Incremental Load

---

# Upcoming Features

- Incremental Merge/Upsert
- Small File Simulation
- Lakehouse Health Metrics
- Snapshot Management
- Data File Compaction
- FastAPI Backend
- Claude AI Agent
- React Dashboard
- AI Maintenance Copilot

---

# Author

**Shrijal Sthapit**

Lakehouse Maintenance Copilot – Bootcamp Capstone Project