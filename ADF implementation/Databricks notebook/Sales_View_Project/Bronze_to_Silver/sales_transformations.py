# Databricks notebook source
# MAGIC %md
# MAGIC #importing Utils notebok

# COMMAND ----------

# MAGIC %run "/Workspace/Sales_View_Project/Bronze_to_Silver/Utils"
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #Mounting storage and loading dataset

# COMMAND ----------

sales_path = "/mnt/bronze/sales_view/sales/"
sales_df = read_csv_file(sales_path)


# COMMAND ----------

sales_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #Transformations

# COMMAND ----------

import re


sales_df = sales_df.toDF(*[re.sub(r'[^A-Za-z0-9]+', '_', re.sub(r'([^A-Z]*[A-Z][^A-Z]*)([A-Z])', r'\1 \2', col)).lower() for col in sales_df.columns])

sales_df.display()

# COMMAND ----------

sales_df.select("customer_id", "order_id", "product_id").distinct().count()


# COMMAND ----------

sales_df.select("customer_id", "product_id").distinct().count()

# COMMAND ----------

sales_df.select("order_id", "product_id").distinct().count()

# COMMAND ----------

# MAGIC %md
# MAGIC #Writing data frame

# COMMAND ----------

delta_table_path = "/mnt/silver/sales_view/customer_sales"

# Write the DataFrame to a Delta table
sales_df.write.format("delta").mode("overwrite").save(delta_table_path)