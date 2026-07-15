# 📊 YouTube Analytics Pipeline

An end-to-end Analytics Engineering project that extracts data from the YouTube Data API, stores it in Google BigQuery, transforms it using dbt, and visualizes business insights through Looker Studio dashboards.

---

## 🚀 Project Overview

This project demonstrates how to build a modern ELT (Extract, Load, Transform) pipeline using Python, BigQuery, dbt, and Looker Studio.

The pipeline automatically extracts metadata from YouTube channels, loads the data into BigQuery, transforms it into analytics-ready models using dbt, and presents business insights through interactive dashboards.

---

## 🛠️ Tech Stack

- Python
- YouTube Data API v3
- Google BigQuery
- dbt (Data Build Tool)
- Looker Studio
- Git & GitHub
- Apache Airflow *(Planned)*

---

## 📂 Project Architecture

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/4814ac9f-0bf8-45c4-8afc-8c3e957ef047" />


# 📁 Project Structure

```
youtube-pipeline/

│
├── config/
│
├── data/
│
├── src/
│   ├── extract/
│   ├── load/
│   └── utils/
│
├── youtube_analytics/
│   ├── models/
│   │    ├── staging/
│   │    ├── intermediate/
│   │    └── marts/
│   │
│   └── macros/
│
├── extract.py
├── load.py
├── main.py
├── resolve_channels.py
├── requirements.txt
└── README.md
```

---

# 🔄 Pipeline Flow

## 1. Resolve Channel Information

Initially, only the YouTube channel handles are available.

The pipeline resolves each handle into:

- Channel ID
- Upload Playlist ID

These details are stored in a YAML configuration file.

---

## 2. Data Extraction

Python scripts extract data from the YouTube Data API.

The following entities are collected:

- Channels
- Videos
- Comments
- Playlists
- Playlist Items
- Categories

The extracted data is stored locally as JSON files.

---

## 3. Data Loading

The JSON files are loaded into BigQuery.

Each entity follows a two-layer loading strategy:

```
JSON
   │
   ▼
Stage Table
   │
   ▼
Raw Table
```

The Stage table stores only the current execution's data.

The Raw table stores the latest version of every record using an idempotent merge strategy.

---

## 4. Data Transformation (dbt)

The raw data is transformed using dbt into analytics-ready models.

### Staging

- Data cleaning
- Data type conversions
- Column standardization

### Intermediate

- Business metric calculations
- Data enrichment
- Engagement metrics

### Marts

Dimension Tables

- dim_channel
- dim_video
- dim_category
- dim_playlist

Fact Tables

- fct_video_daily
- fct_channel_daily

Business reporting models are created on top of these tables for dashboarding.

---

# 📈 Dashboard

The dashboard provides insights into:
<img width="1439" height="912" alt="image" src="https://github.com/user-attachments/assets/25b458dd-d4ae-4a1a-abd7-a751d797ca78" />


## Executive Overview

- Total Views
- Total Likes
- Total Comments
- Total Subscribers
- Total Videos

---

## Growth Analysis

- Daily Subscriber Growth
- Daily View Growth
- Daily Like Growth
- Daily Comment Growth

---

## Video Performance

- Top Performing Videos
- Most Viewed Videos
- Highest Engagement Videos

---

## Channel Insights

- Channel Comparison
- Video Category Distribution
- Publishing Trends

---

## Correlation Analysis

- Video Duration vs Views
- Video Duration vs Likes
- Video Duration vs Engagement Rate

---

# 📊 Data Model

The project follows a dimensional modeling approach.

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

# 📌 Key Features

- End-to-End ELT Pipeline
- Incremental Loading
- Idempotent Merge Logic
- Historical Snapshot Tracking
- Dimensional Data Modeling
- Interactive Dashboard
- Modular Python Code
- dbt Transformations

---

# 🔮 Future Enhancements

- Apache Airflow Orchestration
- Data Quality Tests
- Automated Monitoring & Alerts

---

# 📷 Project Presentation

Presentation Slides:

https://docs.google.com/presentation/d/1kVnb33L0RyrW8bc919-NNJmZ6dJFcpADNYU6r_liWoI/edit?slide=id.g3f4afccb43a_2_647#slide=id.g3f4afccb43a_2_647

---

# 📊 Live Dashboard

Looker Studio Dashboard:

https://datastudio.google.com/reporting/c863200d-9775-41d8-878a-e63c9056a257/page/AMO3F

---

# 👨‍💻 Author

**Kaushik Bendalam**

GitHub:
https://github.com/Kausheeee
