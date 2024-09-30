# Databricks notebook source
# MAGIC %md
# MAGIC #Module Imports 

# COMMAND ----------

from delta.tables import DeltaTable
from pyspark.sql.functions import col
from pyspark.sql import DataFrame
from pyspark.sql.functions import date_format, col
import re
from delta.tables import DeltaTable


# COMMAND ----------

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

# MAGIC %md
# MAGIC ##Write DataFrame to Parquet

# COMMAND ----------

def write_to_parquet(df, path, mode='overwrite'):
    """
    Write a DataFrame to a Parquet file.

    Parameters:
    df (DataFrame): The DataFrame to write.
    path (str): The path to save the Parquet file.
    mode (str): Write mode (e.g., 'overwrite', 'append').
    """
    df.write.parquet(path, mode=mode)


# COMMAND ----------

# MAGIC %md
# MAGIC ##Write DataFrame to Delta Lake

# COMMAND ----------


def upsert_to_delta(df, table_name, merge_condition, silver_base_path="/mnt/silver/sales_view"):
    """
    Performs an upsert (merge) operation into a Delta table in the silver layer.

    Args:
        df (DataFrame): The DataFrame containing new data to be upserted.
        table_name (str): The name of the target table (e.g., 'customer').
        merge_condition (str): The condition for merging records (e.g., 'tgt.customer_id = src.customer_id').
        silver_base_path (str): The base path of the silver layer (default: '/mnt/silver/sales_view').

    Returns:
        None
    """
    # Define the path to the Delta table
    silver_table_path = f"{silver_base_path}/{table_name}"

    # Check if the Delta table exists
    if DeltaTable.isDeltaTable(spark, silver_table_path):
        # Load the existing Delta table
        delta_table = DeltaTable.forPath(spark, silver_table_path)
        
        # Perform the merge (upsert) operation
        delta_table.alias("tgt") \
            .merge(df.alias("src"), merge_condition) \
            .whenMatchedUpdateAll() \
            .whenNotMatchedInsertAll() \
            .execute()
    else:
        # If the Delta table does not exist, write the DataFrame as a new Delta table
        df.write.format("delta").mode("overwrite").save(silver_table_path)
    
    print(f"Upsert operation completed for table: {table_name}")



# COMMAND ----------

# MAGIC %md
# MAGIC ##Write DataFrame to **CSV**

# COMMAND ----------

def write_to_csv(df, path, mode='overwrite', header=True):
    """
    Write a DataFrame to a CSV file.

    Parameters:
    df (DataFrame): The DataFrame to write.
    path (str): The path to save the CSV file.
    mode (str): Write mode (e.g., 'overwrite', 'append').
    header (bool): Whether to write the header.
    """
    df.write.csv(path, mode=mode, header=header)


# COMMAND ----------

# MAGIC %md
# MAGIC ##SNAKE CASE CONVERTER FUNCTION 

# COMMAND ----------



def snake_case_converter(df):
    return df.toDF(*[col.lower().replace(' ', '_').lower() for col in df.columns])


# COMMAND ----------

# MAGIC %md
# MAGIC ## yyyy-MM-dd format function 

# COMMAND ----------



def convert_multiple_date_formats(df: DataFrame, date_columns: list) -> DataFrame:
    """
    Converts the specified date columns to the 'yyyy-MM-dd' format.

    Parameters:
    df (DataFrame): The input DataFrame containing the date columns.
    date_columns (list): A list of column names to format as 'yyyy-MM-dd'.

    Returns:
    DataFrame: A DataFrame with the specified date columns formatted to 'yyyy-MM-dd'.
    """
    # Check if all columns exist in the DataFrame
    for date_column in date_columns:
        if date_column not in df.columns:
            raise ValueError(f"The DataFrame does not contain a '{date_column}' column.")
    
    # Create a new DataFrame with the formatted date columns
    formatted_df = df.select(
        *[
            date_format(col(date_column), "yyyy-MM-dd").alias(date_column) if date_column in date_columns else col(date_column)
            for date_column in df.columns
        ]
    )
    
    return formatted_df

# COMMAND ----------

# MAGIC %md
# MAGIC #Write function

# COMMAND ----------

from delta.tables import DeltaTable

def upsert_to_delta(df, path, table_name, join_key):
    """
    Function to upsert (merge) data into a Delta table.

    Parameters:
    df           : DataFrame     -> The DataFrame to upsert.
    table_name   : str           -> The name of the Delta table (e.g., 'customer').
    join_key     : str           -> The primary key to use for the merge (e.g., 'customer_id').

    Returns:
    None
    """
    
    # Define the location once
    location = path + table_name

    if DeltaTable.isDeltaTable(spark, location):
        print("Upsert executed")
        # If the table exists, perform an upsert using a merge operation
        delta_table = DeltaTable.forPath(spark, location)

        delta_table.alias('target') \
            .merge(
                df.alias('source'),
                f"target.{join_key} = source.{join_key}"  # Define how to match records
            ) \
            .whenMatchedUpdateAll() \
            .whenNotMatchedInsertAll() \
            .execute()

    else:
        print("Created Delta")
        # Write the DataFrame as a Delta table
        df.write.mode('overwrite').format("delta").save(location)
