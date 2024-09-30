# Databricks notebook source
# MAGIC %run "/Workspace/Sales_View_Project/Bronze_to_Silver/Utils"
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #Module imports

# COMMAND ----------

from pyspark.sql import DataFrame
from pyspark.sql.functions import when, col


# COMMAND ----------

# MAGIC %md
# MAGIC #Mounting storage and loading dataset

# COMMAND ----------

product_path = "/mnt/bronze/sales_view/product/"
product_df = read_csv_file(product_path)


# COMMAND ----------

# MAGIC %md
# MAGIC #Transformations

# COMMAND ----------

categories = {1: "Smartphones", 2: "Tablets", 3: "Laptops", 4: "Wearables", 5: "Other"}

df_with_sub_category = product_df.withColumn(
    "sub_category", 
    when(col("category_id") == 1, categories[1])
    .when(col("category_id") == 2, categories[2])
    .when(col("category_id") == 3, categories[3])
    .when(col("category_id") == 4, categories[4])
    .otherwise(categories[5])
)


# COMMAND ----------

df_final_product = snake_case_converter(df_with_sub_category)
df_final_product.display()


# COMMAND ----------

# MAGIC %md
# MAGIC #Writing data frame

# COMMAND ----------

upsert_to_delta(df_final_product, "/mnt/silver/sales_view/","product", "product_id")
   