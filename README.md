# Dynamic Dashboard API Project

## **Objective**
The objective of this project is to create **APIs** to fetch information from the **data warehouse** for **dynamic dashboard creation**.  

The dashboard will allow selecting **dimensions** (e.g., agent or manager) and **aggregation metrics** (e.g., total leads, average conversion rate, average call duration) to visualize data efficiently.

---

## **Architecture**

![img.png](img.png)

**Note:** Green-marked portions indicate the modules being implemented in this project. The design is built with **scalability** in mind.

**Architecture Overview:**
- Events are generated when an **agent ends a call**.  
- These events are sent to a **Pub/Sub** or messaging queue.  
- Events are ingested into the **BigQuery data warehouse** (for now using CSV/JSON files for simulation).  
- **FastAPI** services query the data warehouse to provide results to the dynamic dashboard.  
- **Streamlit** is used to render the dashboard UI.

---

## **Tools & Technologies**
- **Python** – Backend API development  
- **BigQuery** – Data warehouse (using CSV files initially)  
- **SQL / JSON** – Data simulation and querying  
- **FastAPI** – API framework  
- **Streamlit** – Dashboard frontend

---

## **Data Warehouse Mapping**

The warehouse is designed to support **fast aggregations** for agents and managers.  

| **Column Name**  | **Data Type** | **Description** |
|-----------------|---------------|-----------------|
| lead_id          | STRING        | Unique lead identifier |
| assigned_by      | STRING        | Manager who assigned the lead |
| assigned_to      | STRING        | Agent handling the lead |
| assigned_date    | DATE          | Date of assignment |
| status           | STRING        | Current status of the lead (`converted_yes`, `converted_no`, `followup_pending`) |
| call_duration    | FLOAT         | Duration of the call in seconds |
| call_status      | STRING        | Status of the call (`answered` or `missed`) |
| is_hot           | BOOLEAN       | 1 if the lead is hot, otherwise 0 |
| is_warm          | BOOLEAN       | 1 if the lead is warm, otherwise 0 |
| is_cold          | BOOLEAN       | 1 if the lead is cold, otherwise 0 |

> This schema is sufficient to perform aggregations like **total calls**, **conversion rates**, and **lead type analysis**.

---

## **APIs**
*To be implemented.*