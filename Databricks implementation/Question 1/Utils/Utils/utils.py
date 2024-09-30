# Databricks notebook source
import re

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

def write_csv_file(df, file_path):
    df.write.mode('overwrite').csv(file_path)
    print("done")

# COMMAND ----------


def camel_2_snake(name):
    """Insert underscores between each capital letter, treating 'ID' as a single unit."""
    # Replace occurrences of 'ID' with a placeholder
    name = name.replace('ID', 'Id')

    # Use regex to insert underscores between capital letters
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name)

    # Restore 'ID' from the placeholder
    name = name.replace('id', 'ID')

    return name.lower()



def convert_columns(df):
    # Create a list of new column names
    new_columns = [camel_2_snake(col) for col in df.columns]  # Use a list comprehension instead of a generator
    # Ensure the number of new column names matches the number of old ones
    if len(new_columns) != len(df.columns):
        raise ValueError(f"Column count mismatch: old count={len(df.columns)}, new count={len(new_columns)}")
    # Rename the columns using toDF with unpacking operator
    temp_df = df.toDF(*new_columns)
    return temp_df