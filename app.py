from flask import Flask, render_template, request, jsonify
import json
import requests
import mysql.connector
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ethish@123'
app.config['MYSQL_DB'] = 'cve_project'

# Setup logging
logging.basicConfig(filename='cve_sync.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL Database Connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None

# Function to fetch CVEs from the API
def fetch_cves(page=1, results_per_page=10):
    base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    params = {
        'startIndex': (page - 1) * results_per_page,
        'resultsPerPage': results_per_page
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

# Function to check if CVE exists in the database
def cve_exists(cve_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM cve_data WHERE cve_id = %s", (cve_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] > 0

# Function to insert CVE into the database
def insert_cve_data(cve_id, description, published_date, last_modified_date, cvss_score, cvss_vector, severity, vulnerability_status, references_data, weaknesses, configurations, raw_data):
    if cve_exists(cve_id):
        logging.info(f"CVE {cve_id} already exists in the database.")
        return
    
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(''' 
                INSERT INTO cve_data (cve_id, description, published_date, last_modified_date, cvss_score, cvss_vector, severity, vulnerability_status, references_data, weaknesses, configurations, raw_data) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ''', ( 
                cve_id, 
                description, 
                published_date, 
                last_modified_date, 
                cvss_score, 
                cvss_vector, 
                severity, 
                vulnerability_status, 
                json.dumps(references_data),  
                json.dumps(weaknesses),      
                json.dumps(configurations),   
                json.dumps(raw_data)          
            )) 
            connection.commit()
            logging.info(f"CVE {cve_id} inserted successfully.")
        except mysql.connector.Error as err:
            logging.error(f"Error inserting CVE {cve_id}: {err}")
        finally:
            connection.close()

# Test connection route
@app.route('/')
def test_connection():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        connection.close()
        return f"Connected to MySQL, version: {version[0]}"
    else:
        return "Error connecting to MySQL"

# Home route
@app.route("/home")
def home():
    return render_template('home.html')

# Route to sync CVEs
@app.route('/sync_cves')
def sync_cves():
    page = 1
    results_per_page = 10
    while True:
        data = fetch_cves(page, results_per_page)
        if data and 'vulnerabilities' in data:
            cve_items = data['vulnerabilities']
            if len(cve_items) == 0:
                break

            for item in cve_items:
                cve_data = item['cve']
                cve_id = cve_data['id']
                description = next((desc['value'] for desc in cve_data['descriptions'] if desc['lang'] == 'en'), '')
                published_date = cve_data['published']
                last_modified_date = cve_data['lastModified']
                cvss_score = 0
                cvss_vector = ''
                severity = ''
                vulnerability_status = ''
                references_data = cve_data.get('references', [])
                weaknesses = cve_data.get('weaknesses', [])
                configurations = cve_data.get('configurations', {})
                raw_data = cve_data

                insert_cve_data(cve_id, description, published_date, last_modified_date, cvss_score, cvss_vector, severity, vulnerability_status, references_data, weaknesses, configurations, raw_data)
            
            page += 1
        else:
            break

    return render_template('sync_cves.html', message="CVE data synced successfully!")

# Route to display list of CVEs
@app.route('/cves/list')
def cve_list():
    page = int(request.args.get('page', 1))
    results_per_page = int(request.args.get('results_per_page', 10))
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    offset = (page - 1) * results_per_page
    cursor.execute("SELECT cve_id, description, published_date, last_modified_date FROM cve_data LIMIT %s OFFSET %s", (results_per_page, offset))
    cve_data = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) AS total FROM cve_data")
    total_records = cursor.fetchone()['total']
    connection.close()
    
    total_pages = (total_records // results_per_page) + (1 if total_records % results_per_page > 0 else 0)
    
    return render_template('cve_list.html', cve_data=cve_data, page=page, total_pages=total_pages, results_per_page=results_per_page)

# Route to display CVE details
@app.route('/cves/<cve_id>')
def cve_details(cve_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cve_data WHERE cve_id = %s", (cve_id,))
    cve = cursor.fetchone()
    connection.close()
    
    if not cve:
        return f"CVE {cve_id} not found", 404
    
    return render_template('cve_details.html', cve=cve)

if __name__ == "__main__":
    app.run(debug=True)
