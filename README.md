# 🚀 Rocket Launcher Data Pipeline using Apache Airflow

## 📌 Project Overview

This project implements an automated **data pipeline using Apache Airflow** to collect information about **upcoming rocket launches** and download rocket images.

The pipeline retrieves launch data from the **Launch Library 2 API**, processes the response, extracts rocket image URLs, and downloads the corresponding images. The system also stores the launch metadata as a **JSON file** for further analysis.

This automation helps aggregate rocket launch information in a single place and maintain a dataset of rocket launch images.

---

# 🎯 Objective

The objective of this project is to build an automated pipeline that:

- Collects upcoming rocket launch data from an external API
- Extracts relevant launch information
- Stores launch metadata in JSON format
- Downloads rocket images
- Automates the workflow using Apache Airflow scheduling

---

# 📊 Data Source

The dataset used in this project comes from the **Launch Library 2 API**, which provides information about historical and upcoming rocket launches.

### API Endpoint

```
https://ll.thespacedevs.com/2.0.0/launch/upcoming
```

### Data Provided by API

The API response contains information such as:

- Launch ID
- Rocket name
- Launch date and time
- Launch window
- Rocket image URL
- Additional launch metadata

---

# ⚙️ Pipeline Workflow

The Airflow DAG performs the following steps:

1. **Fetch Launch Data**  
   Retrieve upcoming rocket launch data from the Launch Library API.

2. **Store JSON Data**  
   Save the API response as a JSON file.

3. **Extract Image URLs**  
   Parse the JSON data to extract rocket image URLs.

4. **Download Rocket Images**  
   Download rocket images using the extracted URLs.

5. **Store Output Files**  
   Save both metadata and images in the output directory.

---

# 🔄 Pipeline Flow

```
Launch Library API
        │
        ▼
Fetch Launch Data
        │
        ▼
Store Launch Metadata (JSON)
        │
        ▼
Extract Rocket Image URLs
        │
        ▼
Download Rocket Images
        │
        ▼
Store Images in Output Directory
```

---

# ⏰ Airflow Scheduling

The pipeline is scheduled to run automatically on:

**Monday, Wednesday, and Friday at 06:00 AM**

### Cron Expression

```
0 6 * * 1,3,5
```

### Cron Format

```
Minute Hour Day_of_Month Month Day_of_Week
```

| Field | Value | Description |
|------|------|-------------|
| Minute | 0 | At minute 0 |
| Hour | 6 | At 6 AM |
| Day of Month | * | Every day |
| Month | * | Every month |
| Day of Week | 1,3,5 | Monday, Wednesday, Friday |

---

# 📁 Project Structure

```
Rocket_launcher
│
├── config/                     # Configuration files
│
├── dags/                       # Apache Airflow DAG files
│   └── rocket_dag.py
│
├── docker/                     # Docker configuration for Airflow
│
├── output/
│   └── rocket_output/
│       ├── launches.json       # Rocket launch metadata
│       └── images/             # Downloaded rocket images
│           ├── image_0.jpg
│           ├── image_1.jpg
│           ├── image_2.jpg
│           └── image_3.jpg
│
└── README.md
```

---

# 🖼 Output

The pipeline generates two types of outputs.

## 1️⃣ Launch Metadata (JSON)

The rocket launch data retrieved from the API is stored as a JSON file.

```
output/rocket_output/launches.json
```

The JSON file contains:

- Launch ID
- Rocket name
- Launch date
- Launch window
- Image URL
- Additional launch metadata

---

## 2️⃣ Rocket Images

Rocket images are downloaded using the extracted image URLs and stored in:

```
output/rocket_output/images/
```

Example output files:

```
image_0.jpg
image_1.jpg
image_2.jpg
image_3.jpg
```

Each image corresponds to a rocket from the upcoming launch dataset.

---

# 🛠 Technologies Used

| Technology | Purpose |
|-----------|--------|
| Python | Data processing and scripting |
| Apache Airflow | Workflow orchestration |
| Docker | Containerized Airflow environment |
| REST API | Data retrieval |
| JSON | Data format |

---

# 📈 Apache Airflow Concepts Demonstrated

This project demonstrates several important Apache Airflow concepts:

- DAG (Directed Acyclic Graph)
- Task scheduling
- PythonOperator
- Task dependencies
- Cron-based workflow automation
- Data pipeline orchestration

---

# 🚀 How to Run the Project

### 1️⃣ Start the Airflow Environment

Start the Airflow environment using Docker.

### 2️⃣ Place DAG File

Ensure the DAG file is located in the `dags/` directory.

### 3️⃣ Start Airflow Services

Start the Airflow webserver and scheduler.

### 4️⃣ Trigger the DAG

Open the **Airflow UI** and trigger the pipeline.

### 5️⃣ Verify Output

After successful execution, the outputs will be stored in:

```
output/rocket_output/
```

---

# 📌 Conclusion

This project demonstrates how **Apache Airflow can automate a data pipeline that collects, processes, and stores data from an external API**.

The pipeline automates the process of retrieving rocket launch data, storing metadata, downloading rocket images, and scheduling the workflow using Airflow.
