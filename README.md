# Data Engineering assignment
This project provides a comprehensive end-to-end solution for Medallion structure ETL using ADF and Databricks as well as fetching Data from api end point




# ADF Implementation

The data flow process is orchestrated using ADF pipeline, with and parent and child pipelines to move latest files from each folder and coopy to correspondind destination folders in destination container:

<details>
  <summary><strong>1. ADF Pipeline Implementation (with diagrams and explanation)</strong></summary>
  
  ### Creating Parent Pipeline
  ![Creating Parent Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/parent%20pipeline.png)
  In the parent pipeline, I iterate over the sales-view-devtst container to get the metadata at the container level, which will result in the folders [customer, product, sales store] as child items that will be passed into the execute pipeline activity which runs the child pipeline. 
  
  ### Creating Child Pipeline
  ![Creating Child Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/child%20pipeline.png)
  The child pipeline takes the current item in the forEach activity and passes it into the pipeline level parameter that I have configured for the child Pipeline. The current folder is passed to the getMetadata activity inside the forEach activity of the child pipeline, resulting in an array of child items with the lastModified date and file name.
  
  ### Inside forEach Activity in Child Pipeline
  ![Inside forEach Activity in Child Pipeline](https://raw.githubusercontent.com/shamsaravaiah/DE-assignment-implementation/main/ADF%20implementation/Screenshots/inside%20forEach%20activity%20of%20child%20pipeline.png)
  I have assigned a pipeline level variable and assigned an old date value. Inside the forEach activity of the child pipeline, I compare the date variable with the lastModified of the current file. If greater, I swap the date variable with lastModified to preserve the latest date. I then assign the filename to a variable using the SetVariable activity. Then I copy the file to the destination using the latest file name with the Copy Data activity. The aim is to extract fresh and latest files from the source and copy them to the destination.

</details>

<details>
  <summary><strong>2. Resources I have used for the ADF implementation</strong></summary>
  - ADF (data flow orchestration)
  - ADLS Gen 2 (storage purpose, hierarchical namespace)
  - Databricks (to perform transformations on the source datasets prior to saving in the next layer, Implemented medallion architecture to process the files applying the mentioned transformations and writing them as Delta tables using Upset operation)
</details>






# Databricks Implementation

<details>
  <summary><strong>3. assignment 1</strong></summary>
  Implemented the mentioned transformation, using UDF functions and writing a fact table into DBFS as delta table which can be queried on using the mentioned requirements.
    Link: [GitHub Repository](https://github.com/shamsaravaiah/DE-assignment-implementation/tree/main/Databricks%20implementation/Question%201)

  
    
</details>

<details>
  <summary><strong>4. assignment 2</strong></summary>
  Extracted data from an api end point and performed transforamtions and flattening the data set. And wrote it into DBFS as delta table
  Link: [GitHub Repository](https://github.com/shamsaravaiah/DE-assignment-implementation/tree/main/Databricks%20implementation/Question%202)
  <details>
  <summary><strong>1. API Data Pulling Flow Chart</strong></summary>
  <img src="https://github.com/shamsaravaiah/DE-assignment-implementation/blob/main/Databricks%20implementation/Question%202/flow%20diagram.png" alt="API Data Pulling Flow Chart">
    

1. **Constants and Utility Functions:**  
   The notebook begins by defining necessary constants and utility functions.

2. **Data Fetching:**  
   The `fetch_data` function sends an HTTP GET request to the API URL. It logs any errors if the request fails. On success, the function returns the JSON response for further processing.

3. **Data Processing:**  
   The `process_data` function checks if the response contains the expected data structure (a list of users). It logs the number of records if valid or warns of errors if not.

## Data Transformation in Spark

1. **Creating a Spark DataFrame:**  
   The processed data is converted into a Spark DataFrame (`api_df`). The data is displayed to verify successful loading.

2. **Extracting Domain from Email:**  
   A user-defined function (UDF), `extract_domain`, is created using the Python `re` library to extract domain names from email addresses. This UDF generates a new column called `site_address`, which holds the extracted domains.

3. **Adding a Date Column:**  
   The `add_date_column` function is called to append a date column (defined in the utils module).

## Saving Data

The final transformed DataFrame is saved in Delta format using Delta Lake technology. The output path is dynamically generated based on the specified database and table names.

## Listing Files

The notebook concludes by listing the files stored in the output path using `dbutils.fs.ls` and prints the file names.

</details>

</details>

# Answeres to quesitons

<details> 
  <summary><strong>3. What is Data Profiling?</strong></summary>
Data profiling is the process of checking and analyzing data to understand what it looks like, assess its quality, and check how good it is. This helps identify patterns, errors, and the overall quality of the data.

For the provided data, the data profiling steps that were done include:

Check Column Headers: Ensure all column headers are in snake case and lowercase.
Identify Patterns: Analyze and create new columns based on existing data (e.g., splitting names, extracting domains from emails).
Assess Data Types: Convert data types where necessary (e.g., date formats to yyyy-MM-dd).
Validate Values: Check and categorize values (e.g., expenditure status based on spending amounts).
Identify and Handle Anomalies: Ensure data consistency and correctness through transformations and checks.
Dynamic File Assessment: Continuously monitor and retrieve the latest modified files in the ADLS.
Transform Data: Apply rules for data transformation based on profiling insights (e.g., creating subcategories, store categories).
</details>

<details>
  <summary><strong>3. End-to-End Understanding</strong></summary>
Based on my understanding, the use case was designed to implement a structured data processing pipeline using Azure Data Lake Storage (ADLS) and Azure Data Factory (ADF) for sales data analysis. It involves extracting fresh files that are being loaded, transforming, and loading (ETL) data from various sources into a bronze layer for raw storage, a silver layer for processed data, and a gold layer for analytical insights. This setup enables real-time data processing, improved data quality, and enhanced decision-making through consolidated sales reports.

The use case uses the Medallion Architecture pattern, which consists of three layers:

Bronze Layer: Raw data storage where all incoming data is initially ingested without significant transformations. This serves as the source of truth.

Silver Layer: Processed data that has undergone cleaning and transformation. This layer is used for more refined analytics. In my use case, it contains semi-processed/partially cleaned data.

Gold Layer: The final, curated data. In my use case, it contains the StoreProductSalesAnalys data, used for reporting and analytics. It provides high-level insights and can be considered as the data mart. In my use case, I created a large table that can be queried in many ways to derive insights.

This layered approach facilitates incremental data processing and enhances data quality while allowing for flexible analytics across different stages of the data lifecycle, making data available for different workloads.

</details>

