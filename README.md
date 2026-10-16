# Advanced Python ETL Pipeline — Data Engineering Project

## 1. Project Overview

This project demonstrates a simple, reliable ETL (Extract, Transform, Load) pipeline using Python, SQLite, and automated unit testing.

The pipeline processes data records, validates their structure, cleans text fields, rejects invalid or duplicate records, and loads valid data into a SQLite database. It also uses unit tests to verify data transformation and database loading behavior.

The project focuses on essential Data Engineering concepts such as data quality, error handling, database transactions, idempotent loading, and automated testing.

## 2. Project Objectives

- Build a structured ETL workflow using Python.
- Validate incoming records before database insertion.
- Normalize inconsistent text data.
- Identify missing fields and duplicate IDs.
- Load records into SQLite using SQL UPSERT.
- Prevent duplicate database rows when the same data is processed repeatedly.
- Verify pipeline functions using Python's `unittest` framework.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL logic and data processing |
| SQLite | Relational database storage |
| SQL | Database schema and UPSERT operations |
| unittest | Automated unit testing |
| sqlite3 | Python interface for SQLite |

**Requirements:** Python 3.10 or later is recommended. The project uses Python's standard library and does not require external packages.

## 4. System Architecture

```text
Incoming JSON Records
         |
         v
  Data Transformation
         |
         v
  Data Validation
         |
         +--------------------+
         |                    |
         v                    v
   Valid Records        Rejected Records
         |
         v
   SQLite Database
         |
         v
  Verify Database Results
         |
         v
   Automated Unit Tests
```

The supplied test file tests the transformation and database-loading functions independently. It does not automatically call the external API.

## 5. Main Components

### A. Data Transformation

The `transform_and_validate()` function processes incoming records.

It performs the following operations:

- Converts record IDs into integers.
- Removes unnecessary whitespace from titles and body text.
- Checks whether required fields are available.
- Rejects non-positive IDs.
- Detects duplicate IDs within the current batch.
- Separates accepted records from rejected records.

Example input:

```python
{
    "id": 1,
    "userId": 2,
    "title": "  Hello   world ",
    "body": " body "
}
```

Expected cleaned title:

```text
Hello world
```

Expected cleaned body:

```text
body
```

### B. Data Validation

The pipeline rejects records that are missing required fields, contain invalid IDs, have empty titles, or duplicate an ID already encountered in the current batch.

Rejected records are returned with a reason explaining why validation failed.

This helps maintain data quality before loading records into a database.

### C. Database Initialization

The `initialize_database()` function creates two tables if they do not already exist.

**`posts` table**

Stores the processed records:

- `post_id` — unique identifier for each post.
- `user_id` — identifier of the user associated with the post.
- `title` — cleaned title.
- `body` — cleaned body text.
- `loaded_at` — timestamp when the record was processed.

**`etl_runs` table**

Stores an audit record for each load operation:

- `run_id` — unique run identifier.
- `started_at` — pipeline run timestamp.
- `fetched_count` — number of input records.
- `valid_count` — number of accepted records.
- `rejected_count` — number of rejected records.
- `upserted_count` — number of records submitted to the UPSERT operation.

### D. Database Loading and Idempotency

The `load_records()` function inserts valid records into SQLite.

It uses SQL UPSERT with `post_id` as the primary key. If a record with the same ID already exists, its values are updated instead of creating another row.

This demonstrates **idempotent loading**: processing the same record repeatedly does not create duplicate rows.

The database changes and ETL audit entry are executed within a transaction. If the operation fails, the transaction is rolled back.

### E. Automated Testing

The `tests/test_etl_pipeline.py` file contains four unit tests.

| Test | Expected behavior |
|---|---|
| `test_normalizes_whitespace_and_accepts_valid_row` | Cleans text and accepts valid data |
| `test_rejects_missing_fields` | Rejects incomplete records |
| `test_rejects_duplicate_ids_in_same_batch` | Accepts the first record and rejects the duplicate |
| `test_load_is_idempotent` | Confirms repeated loads do not create duplicate rows |

The tests use an in-memory SQLite database, so the database-loading test does not require a permanent database file.

## 6. How to Run the Tests

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/advanced-python-etl-pipeline.git
cd advanced-python-etl-pipeline
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository name.

### Step 2: Check your Python installation

```bash
python --version
```

### Step 3: Run the unit tests

```bash
python -m unittest discover -s tests -v
```

Expected result: all four tests should pass if `etl_pipeline.py` contains the corresponding functions and the project files are in the correct locations.

## 7. Project Folder Structure

```text
advanced-python-etl-pipeline/
│
├── etl_pipeline.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    └── test_etl_pipeline.py
```

## 8. Example Testing Scenarios

### Scenario 1: Valid record

Input contains an ID, user ID, title, and body.

**Expected result:** The record is accepted and its text fields are normalized.

### Scenario 2: Missing fields

Input contains only an ID.

**Expected result:** The record is rejected because required fields are missing.

### Scenario 3: Duplicate ID

Two records with the same ID occur in one input batch.

**Expected result:** The first record is accepted and the second is rejected.

### Scenario 4: Repeated database load

The same valid record is loaded twice.

**Expected result:** The database contains one row for that ID because the second operation updates the existing record.

## 9. Potential Improvements

The project can be extended with additional Data Engineering features:

- Integrate a REST API for automated data extraction.
- Add pagination and incremental loading checkpoints.
- Export rejected records to a JSON Lines file.
- Add configurable logging and pipeline performance metrics.
- Add a dry-run mode that validates records without saving them.
- Replace SQLite with PostgreSQL or MySQL.
- Orchestrate scheduled runs using Apache Airflow.
- Add integration tests and continuous integration using GitHub Actions.

## 10. Important Limitations

This project demonstrates selected ETL components and their tests. The test file does not test the entire end-to-end pipeline or perform live API extraction.

The database-loading test verifies row-count idempotency for repeated records; it does not test every failure or rollback scenario.

The project is a learning and interview demonstration, not a fully deployed production data platform.

## 11. Interview Discussion Points

Be prepared to explain:

1. What ETL means and why the stages are separated.
2. Why data validation should happen before loading.
3. The difference between rejecting duplicate records in a batch and updating an existing database record.
4. What SQL UPSERT does.
5. Why database transactions are important.
6. How unit testing catches regressions.
7. How you would adapt this pipeline to process millions of records.
8. How you would add incremental loading and Apache Airflow scheduling.

## Conclusion

This project demonstrates practical Python Data Engineering fundamentals through data cleaning, validation, SQL database operations, idempotency, transactions, and automated unit testing. It provides a foundation for extending the workflow into a larger ETL or ELT pipeline.
