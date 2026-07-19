# 📊 YouTube Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Google BigQuery](https://img.shields.io/badge/Google-BigQuery-4285F4?logo=googlecloud)
![dbt](https://img.shields.io/badge/dbt-Analytics%20Engineering-orange)
![Apache Airflow](https://img.shields.io/badge/Apache-Airflow-red?logo=apacheairflow)
![Looker Studio](https://img.shields.io/badge/Looker-Studio-4285F4)
![GitHub](https://img.shields.io/badge/Git-GitHub-black?logo=github)

An end-to-end **Analytics Engineering** project that extracts YouTube data using the **YouTube Data API**, loads it into **Google BigQuery**, transforms it using **dbt**, orchestrates the complete workflow with **Apache Airflow**, and visualizes insights using **Looker Studio**.

---

# 🚀 Project Overview

This project demonstrates how to build a production-style ELT (Extract, Load, Transform) pipeline using modern Analytics Engineering best practices.

The pipeline automatically:

- Extracts metadata from the YouTube Data API
- Stores extracted data as JSON files
- Loads data into Google BigQuery
- Builds analytics-ready models using dbt
- Executes the complete workflow using Apache Airflow
- Runs dbt data quality tests
- Sends automated pipeline success/failure notifications
- Visualizes business insights in Looker Studio

---

# 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| Programming | Python |
| Data Source | YouTube Data API v3 |
| Data Warehouse | Google BigQuery |
| Data Transformation | dbt |
| Workflow Orchestration | Apache Airflow |
| Visualization | Looker Studio |
| Version Control | Git & GitHub |

---

# 🏗️ Project Architecture

> Replace the image below with your updated architecture diagram.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/2603f34a-cb1e-499a-8257-3e5e4583ea94" />

---

# ⚙️ Pipeline Workflow

```
                 Apache Airflow
                        │
                        ▼
          Extract Data from YouTube API
                        │
                        ▼
           Landing Layer (JSON Files)
                        │
                        ▼
        Load into BigQuery Stage Tables
                        │
                        ▼
       MERGE into BigQuery Raw Tables
                        │
                        ▼
            dbt Transformations
     (Staging → Intermediate → Marts)
                        │
                        ▼
                  dbt Tests
                        │
                        ▼
          Looker Studio Dashboard
                        │
                        ▼
    Success / Failure Email Notifications
```

---

# 📁 Repository Structure

```text
youtube-analytics-pipeline/

├── airflow/
│   ├── dags/
│   │   └── youtube_pipeline.py
│   └── requirements.txt
│
├── config/
│
├── data/
│
├── docs/
│
├── src/
│   ├── extract/
│   ├── load/
│   └── utils/
│
├── youtube_analytics/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── macros/
│   └── tests/
│
├── extract.py
├── load.py
├── main.py
├── resolve_channels.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Initial Configuration

Before running the pipeline for the first time, execute the helper script below to resolve YouTube channel handles into Channel IDs.

```bash
python resolve_channels.py
```

This is a **one-time setup** that generates the `channels.yml` configuration file. The pipeline reads Channel IDs directly from this configuration during every execution.

---

# 📥 Data Extraction

The pipeline extracts metadata from the YouTube Data API for one or more configured YouTube channels.

The following entities are collected:

- Channels
- Videos
- Comments
- Playlists
- Playlist Items
- Categories

The extracted data is stored locally as JSON files before loading into BigQuery.

---

# 🗄️ BigQuery Loading Strategy

The project follows a two-layer loading architecture.

```
Landing JSON Files
        │
        ▼
   Stage Tables
(Current Pipeline Run)
        │
        ▼
       MERGE
        │
        ▼
    Raw Tables
(Latest Version)
```

### Stage Tables

- Store data from the current pipeline execution.

### Raw Tables

- Store the latest version of every record.
- Support idempotent MERGE operations.
- Prevent duplicate records.

---

# 🔄 dbt Transformations

The project follows a layered dbt architecture.

## Staging Layer

- Data Cleaning
- Type Casting
- Column Standardization

## Intermediate Layer

- Business Logic
- Metric Calculations
- Data Enrichment

## Mart Layer

### Dimension Tables

- dim_channel
- dim_video
- dim_playlist
- dim_category

### Fact Tables

- fct_video_daily
- fct_channel_daily

The marts layer provides analytics-ready tables for reporting and dashboarding.

---

# 📊 Data Model

```
                    dim_channel
                         │
                         │
dim_category ───── fct_video_daily ───── dim_video
                         │
                         │
                    dim_playlist
```

---

# 🌪️ Apache Airflow Orchestration

Apache Airflow automates the complete ELT workflow.

The DAG performs the following tasks:

- Extract data from the YouTube API
- Load data into BigQuery
- Execute dbt models
- Run dbt tests
- Send pipeline notifications

### Airflow Features

- Manual Execution
- Scheduled Execution
- Task Dependencies
- Retry Mechanism
- Custom Email Notifications
- Failure Monitoring
- Workflow Orchestration

### Airflow DAG

> Add a screenshot of your DAG Graph View.

<img width="1199" height="230" alt="image" src="https://github.com/user-attachments/assets/ed99cf32-deed-4e6d-85b7-cfbe3c091950" />


---

# 📧 Monitoring & Alerts

The pipeline automatically sends email notifications for failed executions.

### Failure Notification

- DAG Name
- Failed Task
- Run ID
- Execution Date
- Exception Details
- Airflow Log Link

Example:

<img width="1456" height="814" alt="image" src="https://github.com/user-attachments/assets/48b69801-3fc1-4208-9346-aa6db40f9fe1" />


---

# 📈 Dashboard

The Looker Studio dashboard provides business insights through multiple analytical views.

### Executive Overview

- Total Views
- Total Likes
- Total Comments
- Total Subscribers
- Total Videos

### Growth Analysis

- Daily Subscriber Growth
- Daily View Growth
- Daily Like Growth
- Daily Comment Growth

### Video Performance

- Top Performing Videos
- Most Viewed Videos
- Highest Engagement Videos

### Channel Insights

- Channel Comparison
- Publishing Trends
- Category Distribution

### Correlation Analysis

- Video Duration vs Views
- Video Duration vs Likes
- Video Duration vs Engagement Rate

Dashboard Preview:

![Dashboard](docs/dashboard.png)

---

# ✨ Key Features

- End-to-End ELT Pipeline
- Modular Python Architecture
- Landing → Stage → Raw Loading Strategy
- Incremental & Idempotent Loading
- Historical Snapshot Tracking
- Dimensional Data Modeling
- dbt Transformations
- dbt Data Quality Tests
- Apache Airflow Orchestration
- Automated Email Notifications
- Interactive Looker Studio Dashboard

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Kausheeee/youtube-analytics-pipeline.git

cd youtube-analytics-pipeline
```

## Create Python Environment

```bash
python -m venv yt-venv

source yt-venv/bin/activate

pip install -r requirements.txt
```

## Create Airflow Environment

```bash
cd airflow

python -m venv airflow-venv

source airflow-venv/bin/activate

pip install -r requirements.txt
```

---

# 📊 Live Dashboard

**Looker Studio Dashboard**

https://datastudio.google.com/reporting/c863200d-9775-41d8-878a-e63c9056a257/page/AMO3F

---

# 📚 Project Presentations

This repository includes two presentation decks that explain the project implementation and architecture.

### 📊 Analytics Engineering Pipeline

Covers the end-to-end ELT pipeline, including:

- YouTube Data API extraction
- BigQuery loading strategy
- dbt transformations
- Data modeling
- Looker Studio dashboard

🔗 https://docs.google.com/presentation/d/1kVnb33L0RyrW8bc919-NNJmZ6dJFcpADNYU6r_liWoI/edit

---

### 🌪️ Apache Airflow Orchestration

Covers the orchestration layer built using Apache Airflow, including:

- Airflow Architecture
- Core Components
- TaskFlow API
- DAG Implementation
- Scheduling
- XCom Communication
- Failure Email Alerts
- Engineering Decisions

🔗 https://docs.google.com/presentation/d/1s8_jcSdVyQDvXpKbczOtc9MCh_PZChb745kE8u9w4BI/edit

---

# 👨‍💻 Author

**Kaushik Bendalam**

GitHub: https://github.com/Kausheeee

LinkedIn: https://www.linkedin.com/in/kaushik-bendalam-650899250

---

⭐ **If you found this project helpful, consider giving it a star!**
