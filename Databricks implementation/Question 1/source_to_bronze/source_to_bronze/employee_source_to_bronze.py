# Databricks notebook source
# MAGIC %run "/Workspace/Utils/utils"

# COMMAND ----------


country_path = "/mnt/emp_mount/Country/Country-Q1.csv"
department_path = "/mnt/emp_mount/Department/Department-Q1.csv"
employee_path = "/mnt/emp_mount/Employee/Employee-Q1.csv"


# Using Spark to read CSV
country_df = read_csv_file(country_path)
department_df = read_csv_file(department_path)
employee_df = read_csv_file(employee_path)







# COMMAND ----------




write_csv_file(department_df, "mnt/source_to_bronze/department.csv")
write_csv_file(employee_df, "mnt/source_to_bronze/employee.csv")
write_csv_file(country_df, "mnt/source_to_bronze/country.csv")

# COMMAND ----------

dbutils.fs.ls("/mnt/source_to_bronze/")

# COMMAND ----------

dbutils.fs.ls("/mnt/source_to_bronze/")