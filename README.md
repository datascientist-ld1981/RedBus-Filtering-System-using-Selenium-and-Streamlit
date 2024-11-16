# RedBus Inter-State Travel Information System 🚌  

## Project Title  
**RedBus Inter-State Travel Information System**  

---

## Problem Statement / Project Description 📝  

Travelers often struggle to find consolidated, real-time data about buses operating across different states, including their availability, pricing, and schedules. The lack of a unified dashboard to visualize this information creates inefficiencies for passengers who need to compare buses and routes.  

This project solves this problem by:  
- Scraping real-time bus data from **RedBus** using **Selenium**.  
- Storing the data in a structured **MySQL database** for querying.  
- Providing a **Streamlit-based dashboard** that allows users to interactively filter, explore, and visualize bus data.  
- Displaying important details such as seat availability, route, and pricing in an easy-to-use interface.  

---

## Features 🚀  

1. **Data Scraping**:  
   - Scrapes bus details from RedBus using the latest version of **Selenium**.  
   - Captures fields such as `bus_name`, `route_name`, `bus_type`, `price`, `departing_time`, `reaching_time`, and `seats_available`.  

2. **Database Integration**:  
   - Data is stored in a **MySQL database** with a structured schema for querying and filtering.  

3. **Streamlit Dashboard**:  
   - Interactive filters for `state`, `route_name`, `bus_name`, and `bus_type`.  
   - Displays results in a table with properly formatted time fields (`departing_time`, `reaching_time`).  

4. **Visualization**:  
   - **Pie chart** showing seat availability by bus name. Buses with no names are grouped as **"Others"**.  

5. **Responsive and Dynamic**:  
   - Only displays relevant filters after selecting a state.  
   - Displays the pie chart only when both `state` and `route_name` are selected.  

---

## Prerequisites 🛠️  

Before you begin, ensure you have the following installed:  
1. **Python 3.7 or higher**  
2. **Selenium WebDriver** (ChromeDriver recommended)  
3. **MySQL Database**  
4. Required Python libraries (install via `requirements.txt`).  

---

## Installation and Usage ⚙️  

### 1. Clone the Repository  
```bash
git clone https://github.com/datascientist-ld1981/redbus-travel-system.git
cd redbus-travel-system

## 2. Project Structure
/redbus-travel-system
    ├── /assets                  # Contains image assets for the dashboard
    ├── /database                # MySQL database and schema files
    ├── /scripts                 # Python scripts (scraping, database interactions)
    │   ├── DataScrapping-Redbus(Pep8&257).ipynb   # Jupyter notebook for scraping RedBus data
    │   ├── config.py            # Database configuration settings
    ├── /dashboard               # Streamlit dashboard source code
    │   ├── redbusStreamlit.py   # Main Streamlit app for visualization
    ├── requirements.txt         # Python dependencies
    ├── README.md                # Project documentation
    └── Table creation query-REDBUS.txt  # MySQL database schema
## 3. Create Table in MYSQL from the text file

## 4. Scrape Data from RedBus
Run the DataScrapping-Redbus(Pep8&257).ipynb Jupyter notebook to collect bus data from the RedBus website and store it in the MySQL database. You can execute this notebook in JupyterLab or Jupyter Notebook:
```bash
jupyter notebook DataScrapping-Redbus(Pep8&257).ipynb

## 5. Start the Streamlit Dashboard
Once the data is scraped and stored in the database, you can start the interactive Streamlit dashboard by running:
```bash
streamlit run redbusStreamlit.py
This will launch the dashboard in your web browser, where you can filter and explore the bus travel data interactively.


GitHub Repository 🔗
https://github.com/datascientist-ld1981




