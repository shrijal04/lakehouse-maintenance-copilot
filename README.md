# 🏔️ Lakehouse Maintenance Copilot

An AI-powered Lakehouse Maintenance Copilot that monitors Apache Iceberg table health, detects lakehouse degradation, visualizes maintenance metrics, and assists users with an AI-powered maintenance assistant.

---

# Project Overview

This project simulates a real-world retail company's modern data platform.

A PostgreSQL OLTP database acts as the operational system where customers place orders.

Apache Spark incrementally ingests this transactional data into Apache Iceberg tables, creating a Lakehouse architecture. Repeated incremental loads intentionally generate many small data files to simulate real production environments.

The system continuously monitors Iceberg table health by collecting metrics such as snapshot count, manifest files, file counts, and storage size. These metrics are exposed through a FastAPI backend and visualized in a Next.js dashboard.

An AI-powered Copilot assists users by answering questions related to Apache Iceberg and lakehouse maintenance. (RAG integration with live lakehouse metrics is the next milestone.)

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

- Groq API
- Llama 3.3 70B Versatile

## Frontend

- Next.js
- React
- Tailwind CSS
- Recharts

---

# Project Structure

```text
lakehouse-maintenance-copilot/

├── backend/
│   ├── app/
│   ├── generators/
│   ├── spark/
│   ├── maintenance/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│
├── docs/
│
└── README.md
```

---

# Project Milestones

---

# ✅ Milestone 1 — PostgreSQL Source System

Built a realistic retail OLTP database.

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

The schema is fully normalized using foreign key relationships to mimic a production transactional database.

---

## Synthetic Data Generation

The entire dataset is automatically generated using Python and Faker.

Generated tables include:

- Categories
- Brands
- Stores
- Products
- Customers
- Orders
- Order Items

Dataset Size

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

# ✅ Milestone 2 — Apache Iceberg Lakehouse

Built an Apache Iceberg Lakehouse using Apache Spark.

Implemented:

- Spark Session
- Iceberg Catalog
- Initial ETL
- Incremental Data Loading
- Snapshot Creation
- Iceberg Table Management

Tables Created

- Orders
- Order Items

Repeated incremental ingestion intentionally creates multiple snapshots and metadata growth to simulate real-world lakehouse degradation.

---

# ✅ Milestone 3 — Lakehouse Health Monitoring

Implemented health monitoring for Iceberg tables.

Health metrics include:

- Snapshot Count
- Data File Count
- Average File Size
- Total Table Size
- Manifest File Count
- Orphan File Count

Each maintenance run stores these metrics in PostgreSQL, allowing historical tracking of table health over time.

---

# ✅ Milestone 4 — FastAPI Backend

Built a REST API for exposing lakehouse information.

Implemented endpoints:

### Health APIs

- `/lakehouse/orders/health`
- `/lakehouse/order-items/health`

### History APIs

- `/lakehouse/orders/history`
- `/lakehouse/order-items/history`

The backend connects Spark, PostgreSQL, and Iceberg to provide real-time health information.

---

# ✅ Milestone 5 — Dashboard

Built an interactive dashboard using Next.js.

Features include:

- Overall lakehouse overview
- Orders table health
- Order Items table health
- Historical health trends
- Interactive charts
- Responsive UI
- Dark theme interface

---

# ✅ Milestone 6 — AI Copilot (Initial Integration)

Integrated an AI assistant using Groq and Llama 3.3.

Current capabilities:

- Answers questions about Apache Iceberg
- Explains Spark concepts
- Explains lakehouse architecture
- Provides maintenance best practices
- Supports Markdown-formatted responses

At this stage, the AI is functioning as a general technical assistant.

⚠️ **RAG (Retrieval-Augmented Generation) has not yet been implemented.**

Currently, the Copilot does **not** access your project's live lakehouse metrics or database.

The current milestone only verifies that:

- Backend AI API works
- Frontend chat interface works
- Groq integration is successful
- End-to-end communication between frontend and backend is functional

The next milestone will provide the AI with real-time context from your Iceberg tables before generating responses.

---

# Running the Project

## Backend

Create a virtual environment.

```bash
cd backend

python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=lakehouse_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

GROQ_API_KEY=your_api_key
```

Start FastAPI.

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Current Progress

## ✅ Completed

- PostgreSQL Source System
- Synthetic Dataset Generator
- Apache Spark Setup
- Apache Iceberg Setup
- Initial ETL
- Incremental Loads
- Iceberg Health Monitoring
- Health History Storage
- FastAPI Backend
- REST APIs
- Dashboard UI
- Health Trend Charts
- AI Copilot Integration (Groq)

---

## 🚧 In Progress

- Retrieval-Augmented Generation (RAG)
- AI access to live Iceberg metrics
- AI-powered maintenance recommendations
- Maintenance execution workflow
- Table compaction automation
- Snapshot expiration
- Orphan file cleanup

---

# Future Enhancements

- Context-aware AI responses
- Automatic maintenance recommendations
- Query optimization suggestions
- Table compaction execution
- Snapshot expiration controls
- Orphan file detection
- Maintenance audit logs
- Multi-table monitoring
- Role-based maintenance approval

---

# Author

**Shrijal Sthapit**

Bootcamp Capstone Project — Lakehouse Maintenance Copilot