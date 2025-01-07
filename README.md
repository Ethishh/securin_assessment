# CVE Management System

A comprehensive web application for synchronizing, storing, and displaying CVE (Common Vulnerabilities and Exposures) data from the NVD (National Vulnerability Database) API. This project provides an intuitive interface to view, sort, and filter CVE data and detailed information about individual CVEs.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Features](#features)
- [Approach](#approach)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Screenshots](#screenshots)


---

## Problem Statement

The goal is to create a system that can:
- Sync CVE data from the NVD API to a MySQL database.
- Display the synchronized data in a paginated, sortable, and filterable interface.
- Allow users to view detailed information about specific CVEs.
- Provide options to customize the number of results per page.

---

## Features

1. **Data Synchronization**: Pulls CVE data from the NVD API and stores it in a MySQL database.
2. **Dynamic UI**:
   - Paginated and sortable tables for CVE data.
   - Customizable results per page (10, 20, 50).
   - Detailed view for each CVE, showing metrics, descriptions, and references.
3. **Flask Framework**:
   - Serves as the backbone of the application for routing, database interaction, and API handling.
   - Provides REST endpoints for dynamic front-end data fetching.
4. **Database Management**:
   - Efficient storage of CVE data with deduplication.
   - Columns for CVE ID, status, published date, last modified date, etc.

---

## Approach

### Logical Flow

1. **Data Fetching**:
   - Use the NVD API to fetch CVE data in JSON format.
   - Paginate API calls to handle large datasets.

2. **Data Storage**:
   - Check if a CVE ID already exists in the database.
   - Insert new data into MySQL, ensuring accurate schema alignment.

3. **Data Display**:
   - Use Flask to create endpoints for fetching paginated and detailed CVE data.
   - Build a responsive front-end with HTML, CSS, and JavaScript.
   - Use AJAX for seamless interactions and dynamic updates.

4. **UI Design**:
   - Design `cve_list.html` for an overview of all CVEs with sorting, filtering, and pagination.
   - Create `cve_details.html` for in-depth details of individual CVEs.

5. **Code Structure**:
   - Use modular functions in Flask for database connectivity, API handling, and data processing.
   - Ensure clean separation of concerns between front-end and back-end.

---

## Technologies Used

### Back-End
- **Flask**: Lightweight Python framework for building web applications and REST APIs.
- **Python**: Core programming language for server-side logic.
- **MySQL**: Relational database for storing CVE data.
- **Logging**: For tracking synchronization and debugging.

### Front-End
- **HTML/CSS**: For UI design.


### APIs
- **NVD API**: For fetching CVE data.

---

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Ethishh/securin_assessment.git
   cd securin_assessment

## Screenshots
