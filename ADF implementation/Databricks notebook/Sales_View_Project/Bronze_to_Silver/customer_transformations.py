# Databricks notebook source
# MAGIC %md
# MAGIC #importing Utils notebok

# COMMAND ----------

# MAGIC %run "/Workspace/Sales_View_Project/Bronze_to_Silver/Utils"
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #Module imports

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType, TimestampType
from pyspark.sql.functions import split, col, when, col, lower, to_date


# COMMAND ----------

# MAGIC %md
# MAGIC # loading dataset

# COMMAND ----------

customer_path = "/mnt/bronze/sales_view/customer/"
customer_df = read_csv_file(customer_path)

customer_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Transformations

# COMMAND ----------

df_Name_split = customer_df.withColumn('first name', split(col('Name'), ' ').getItem(0)) \
                 .withColumn('last name', split(col('Name'), ' ').getItem(1))


    

# COMMAND ----------

df_with_domain_name = df_Name_split.withColumn('Domain_Name', split(split(col('Email Id'), '@').getItem(1), '\.').getItem(0))

# COMMAND ----------

if 'Gender'.lower() not in df_with_domain_name.columns:
        raise ValueError("The DataFrame does not contain a 'gender' column.")

else:
    # Convert gender values
    df_with_gender = df_with_domain_name.withColumn(
        'gender_letter',
        when(lower(col('Gender')).isin(['male', 'm']), 'M')\
        .when(lower(col('Gender')).isin(['female', 'f']), 'F')\
        .otherwise(None)    
    )

# COMMAND ----------

if 'Joining Date' not in df_with_gender.columns:
    raise ValueError("The DataFrame does not contain a 'Joining Date' column.")

else:
    # Split the 'Joining Date' into 'date' and 'time' columns
    df_split_date_time = f_split_date_time = df_with_gender.withColumn(
        'date', to_date(split(col('Joining Date'), ' ').getItem(0), 'yyyy-MM-dd')
    ).withColumn(
        'time', split(col('Joining Date'), ' ').getItem(1)
    )

# COMMAND ----------

if 'spent' not in df_split_date_time.columns:
        raise ValueError("The DataFrame does not contain a 'spent' column.")
else:
    # Create 'expenditure-status' based on the 'spent' column
    df_with_expenditure_status = df_split_date_time.withColumn(
        'expenditure status',
        when(col('Spent') < 200, 'MINIMUM')
        .otherwise('MAXIMUM')
    )

# COMMAND ----------

bronze_customer_df = snake_case_converter(df_with_expenditure_status)


# COMMAND ----------

bronze_customer_df.orderBy("Customer Id").display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Writing data frame

# COMMAND ----------

upsert_to_delta(bronze_customer_df, "/mnt/silver/sales_view/","customer", "customer_id")
   

# COMMAND ----------

dbutils.fs.ls("/user/")

# COMMAND ----------

dbutils.fs.ls('/silver/')

# COMMAND ----------

# Delete the data files directly from the file system
#dbutils.fs.rm("/silver/sales_view/", recurse=True)
