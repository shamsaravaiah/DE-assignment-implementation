# Databricks notebook source
# MAGIC %run "/Workspace/utils"

# COMMAND ----------

import logging
import requests
from pyspark.sql import SparkSession
import re
from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType



# COMMAND ----------



def extract_domain(email):
    """
    Extracts the domain from an email address.
    
    Args:
    email (str): The email address from which to extract the domain.
    
    Returns:
    str: The domain of the email address, or None if the email is invalid.
    """
    try:
        # Define a regex pattern for extracting the domain
        pattern = r'@([a-zA-Z0-9.-]+)$'
        match = re.search(pattern, email)

        if match:
            return match.group(1)  # Return the captured domain
        else:
            return None  # Return None for invalid emails
    except Exception as e:
        print(f"Error processing email '{email}': {e}")
        return None  # Return None if any exception occurs

# COMMAND ----------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
API_URL = "https://reqres.in/api/users?page=2"

def fetch_data(url):
    """Fetch data from the API and return JSON response."""
    try:
        response = requests.get(url)
        # Check if the response status code is not 200
        if response.status_code != 200:
            logger.error(f"Request failed with status code: {response.status_code} - {response.text}")
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return None

def process_data(data):
    """Process the JSON data and create a Spark DataFrame."""
    if 'data' not in data or not isinstance(data['data'], list) or len(data['data']) == 0:

        logger.warning("The 'data' field is either missing or is not a list.")
        return None
    
    users = data['data']
    num_records = len(users)
    
    if num_records == 0:
        logger.info("No records found in the 'data' field.")
        return None

    logger.info(f"Number of records: {num_records}")
    return users


# Fetch data from the API
json_data = fetch_data(API_URL)

if json_data is None:
    logger.error("Failed to fetch data from the API.")
else:
    # Process the fetched data
    users = process_data(json_data)

    if users is not None:
        # Convert to a Spark DataFrame
        api_df = spark.createDataFrame(users)
        api_df.show()

# COMMAND ----------

# Create a UDF from the function
extract_domain_udf = udf(extract_domain, StringType())

# Use the UDF to add a new column 'site_address'
api_df_with_site_address = api_df.withColumn("site_address", extract_domain_udf(api_df["email"]))

final_df = add_date_column(api_df_with_site_address)
# Show the resulting DataFrame
final_df.show(truncate=False)

# COMMAND ----------

db_name = "site_info"
table_name = "person_info"

output_path = f"/{db_name}/{table_name}"

final_df.write.format("delta").mode("overwrite").save(output_path)


# COMMAND ----------

files = dbutils.fs.ls(output_path)

# Display the files
for file in files:
    print(file)
