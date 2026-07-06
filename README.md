# 🏔️ Lakehouse Maintenance Copilot

An AI-powered Lakehouse Maintenance Copilot that monitors Apache Iceberg table health, detects lakehouse degradation, executes maintenance operations, visualizes historical health metrics, and provides an intelligent AI assistant capable of interacting with the lakehouse through MCP (Model Context Protocol) tools.

---

# Project Overview

This project simulates a modern retail company's data platform.

A PostgreSQL OLTP database stores transactional order data. Apache Spark incrementally ingests this data into Apache Iceberg tables, creating a local Lakehouse architecture.

Repeated incremental loads intentionally generate multiple snapshots and metadata growth to simulate real production environments.

The application continuously monitors Iceberg table health by collecting metadata such as:

- Snapshot Count
- Data File Count
- Average File Size
- Manifest File Count
- Total Table Size
- Orphan File Count

Health metrics are stored in PostgreSQL to maintain historical trends.

An AI Copilot powered by Groq + Llama 3.3 can answer questions, inspect table health, detect issues, and request maintenance through MCP tools.

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
- FastMCP (Model Context Protocol)

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
│   ├── maintenance/
│   ├── etl/
│   ├── generators/
│   ├── simulation/
│   ├── spark/
│   ├── requirements.txt
│   └── .venv
│
├── frontend/
│
├── docs/
│
└── README.md
```

---

# System Architecture

```
PostgreSQL
      │
      ▼
Apache Spark
      │
      ▼
Apache Iceberg
      │
      ▼
Health Metrics
      │
      ▼
FastAPI Backend
      │
      ├──────── Dashboard APIs
      │
      └──────── AI Copilot
                     │
                     ▼
               MCP Tool Server
                     │
                     ▼
               Health Tools
               Issues Tools
               Maintenance Tools
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

The schema is normalized using foreign key relationships.

---

## Synthetic Data Generation

Generated using Python and Faker.

Generated tables:

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

Implemented:

- Spark Session
- Iceberg Catalog
- Initial ETL
- Incremental Data Loading
- Snapshot Creation
- Iceberg Metadata
- Iceberg SQL Support

Tables Created

- Orders
- Order Items

Repeated incremental ingestion creates multiple snapshots and metadata growth to simulate real-world lakehouse degradation.

---

# ✅ Milestone 3 — Lakehouse Health Monitoring

Implemented health monitoring for Iceberg tables.

Metrics collected:

- Snapshot Count
- Data File Count
- Average File Size
- Total Table Size
- Manifest File Count
- Orphan File Count

Each health check is stored in PostgreSQL, allowing historical trend analysis.

---

# ✅ Milestone 4 — FastAPI Backend

Built REST APIs exposing lakehouse information.

Implemented endpoints:

## Health

- `/lakehouse/orders/health`
- `/lakehouse/order-items/health`

## History

- `/lakehouse/orders/history`
- `/lakehouse/order-items/history`

## Issues

- Detect unhealthy Iceberg tables

## Maintenance

- Request maintenance
- Confirmation workflow
- Execute maintenance

---

# ✅ Milestone 5 — Dashboard

Built a modern dashboard using Next.js.

Features include:

- Lakehouse Overview
- Health Metrics
- Historical Trend Charts
- Maintenance History
- Interactive Charts
- Responsive Layout
- Dark Theme
- Loading Overlay while fetching data

---

# ✅ Milestone 6 — AI Copilot

Integrated Groq using the Llama 3.3 70B Versatile model.

Capabilities include:

- Apache Iceberg Q&A
- Spark Q&A
- Lakehouse Concepts
- Maintenance Best Practices
- Markdown Responses
- Tool-based responses

---

# ✅ Milestone 7 — MCP Integration

Implemented FastMCP server exposing lakehouse operations as AI tools.

Available MCP Tools

### Health Tool

Returns live Iceberg table health.

Example

```
Health of orders table
```

---

### Issues Tool

Detects health issues.

Example

```
Show issues in order_items
```

---

### Maintenance Tool

Requests maintenance.

Maintenance requires explicit confirmation before execution.

Example

```
Clean the orders table
```

Workflow

```
User
   │
   ▼
Request Maintenance
   │
   ▼
Confirmation Required
   │
   ▼
User Confirms
   │
   ▼
Maintenance Executes
```

---

# ✅ Milestone 8 — Maintenance Workflow

Implemented:

- Rewrite Data Files
- Rewrite Manifest Files
- Snapshot Expiration
- Remove Orphan Files

Maintenance supports:

- orders
- order_items
- both tables together

---

# ✅ Milestone 9 — AI Confirmation Workflow

Implemented confirmation management.

Workflow

```
User
      │
      ▼
Run Maintenance
      │
      ▼
AI Requests Confirmation
      │
      ▼
User replies Yes / No
      │
      ▼
Maintenance Executes or Cancels
```

This prevents accidental destructive operations.

---

# ✅ Milestone 10 — Optimistic Concurrency Conflict Simulation

Implemented a simulation demonstrating Apache Iceberg's optimistic concurrency control.

The simulation creates two independent Spark applications attempting to update the same table simultaneously.

Expected Result

One update succeeds while the second fails with a ValidationException.

Instead of exposing a large Java stack trace, the backend converts the error into a plain English explanation:

> Another user modified the table while maintenance was running. Iceberg stopped this operation to prevent data corruption. No data was lost. You can safely retry the maintenance.

---

# Running the Project

## Backend

Create virtual environment

```bash
cd backend

python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```



Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## MCP Server

Start the MCP server

```bash
python -m app.mcp.server
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
- Dashboard
- Trend Charts
- Loading Overlay
- AI Copilot
- FastMCP Server
- Health Tool
- Issues Tool
- Maintenance Tool
- Confirmation Workflow
- Maintenance Execution
- Optimistic Concurrency Conflict Simulation
- Plain-English Error Explanation

---

## 🚧 In Progress

- Automatic Scheduled Health Checks
- AI Proactive Health Alerts

---

# Stretch Goals

## Automatic Health Monitoring

- Run health checks automatically on a schedule
- Store health history continuously
- Detect unhealthy tables automatically

---

## Proactive AI Alerts

Allow the AI assistant to notify users before they ask.

Example

```
⚠️ The orders table has accumulated many manifest files.

Maintenance is recommended.
```

---

# Future Enhancements

- MCP Client Integration
- Retrieval-Augmented Generation (RAG)
- Context-aware AI responses
- Automatic maintenance recommendations
- Maintenance audit logs
- Multi-table monitoring
- Role-based approvals
- Remote Iceberg Catalog support
- Cloud object storage integration

---

# Author

**Shrijal Sthapit**

Bootcamp Capstone Project

**Lakehouse Maintenance Copilot**