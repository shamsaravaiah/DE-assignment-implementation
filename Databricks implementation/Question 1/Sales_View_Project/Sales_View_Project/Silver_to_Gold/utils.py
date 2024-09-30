# Databricks notebook source
def read_csv_file(file_path,custom_schema=None):
    """
    This function reads a CSV file from the given file path using Spark,
    with the header and schema inferred.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        DataFrame: Spark DataFrame containing the CSV data.
    """
    if custom_schema is None:
        df = spark.read.csv(file_path, header=True, inferSchema=True)
    else:
        # Use Spark to read the CSV file with headers and infer schema
        df = spark.read.csv(file_path, header=True, schema=custom_schema)
    
    return df





# COMMAND ----------

def read_delta_table(file_path):
    """
    This function reads a Delta table from the given file path using Spark.
    
    Args:
        file_path (str): The path to the Delta table.
        
    Returns:
        DataFrame: Spark DataFrame containing the Delta table data.
    """
    # Read the Delta table
    df = spark.read.format("delta").load(file_path)
    return df
