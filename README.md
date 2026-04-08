# bynry_case_study
#  StockFlow Inventory Management Case Study

##  Author

Aditya Mall

---

##  Overview

This repository contains my solution for the **StockFlow B2B Inventory Management Case Study**.

The solution covers:

* Code Review & Debugging
* Database Design
* API Implementation (Low Stock Alerts)

---

##  Tech Stack

* Python (Flask)
* SQLAlchemy
* PostgreSQL (assumed)

---

## Project Structure

* `app.py` → Main Flask app
* `models.py` → Database models
* `api/` → API endpoints
* `docs/` → Detailed explanations for each part
* `database_schema.sql` → SQL schema

---

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

---

## Key Highlights

* Transaction-safe product creation
* Scalable multi-warehouse inventory design
* Low-stock alert system with demand prediction
* Clean and modular API structure

---

## Assumptions

* Recent sales = last 30 days
* SKU is globally unique
* Products can exist in multiple warehouses

---

## 🧠 Future Improvements

* Add authentication (JWT)
* Add caching (Redis)
* Pagination for alerts
* Background jobs for stock prediction

---
