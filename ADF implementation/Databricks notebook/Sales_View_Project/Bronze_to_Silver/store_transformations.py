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

from pyspark.sql import DataFrame
from pyspark.sql.functions import split, col

# COMMAND ----------

# MAGIC %md
# MAGIC #Mounting storage and loading dataset

# COMMAND ----------

store_path = "/mnt/bronze/sales_view/store/"
store_df = read_csv_file(store_path)


# COMMAND ----------

# MAGIC %md
# MAGIC #Transformations

# COMMAND ----------

df_with_domain_name = store_df.withColumn('store category', split(split(col('email_address'), '@').getItem(1), '\.').getItem(0))


# COMMAND ----------

final_store_df = snake_case_converter(df_with_domain_name)
final_store_df = convert_multiple_date_formats(final_store_df, ['created_at', 'updated_at'])
final_store_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Writing data frame

# COMMAND ----------

upsert_to_delta(final_store_df, "/mnt/silver/sales_view/","store", "store_id")
