# Databricks notebook source
# Define the SQL query
sql_query = f'''
SELECT 
    e.employee_id, 
    e.age, 
    e.employee_name, 
    e.salary, 
    d.department_name, 
    c.country_name  
FROM 
    employee_info.dim_employee e 
LEFT JOIN 
    employee_info.dim_department d 
ON 
    e.department = d.department_id 
LEFT JOIN 
    employee_info.dim_country c 
ON 
    e.country = c.country_code
'''

fact_employee_df = spark.sql(sql_query)





# COMMAND ----------

fact_employee_df.displaY()

# COMMAND ----------

from delta.tables import DeltaTable

# Define the path where you want to write the DataFrame
dbfs_path = "/gold/employee/fact_employee"

# Load the existing Delta table if it exists
if DeltaTable.isDeltaTable(spark, dbfs_path):
    delta_table = DeltaTable.forPath(spark, dbfs_path)
    
    # Define the condition for deletion (replace 'your_date_condition' with actual date)
    at_load_date_condition = "at_load_date = 'your_date_condition'"
    
    # Delete records that meet the condition
    delta_table.delete(at_load_date_condition)

# Write the new DataFrame to the specified path in Delta format with overwrite mode
fact_employee_df.write.format("delta").mode("overwrite").save(dbfs_path)


# COMMAND ----------

# Define the path to the existing Delta table
existing_table_path = "/gold/employee/fact_employee"

# Read the existing Delta table
existing_df = spark.read.format("delta").load(existing_table_path)


# COMMAND ----------

fact_employee_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("Employee_info.fact_employee")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     department_name, 
# MAGIC     SUM(salary) AS total_salary
# MAGIC FROM 
# MAGIC     Employee_info.fact_employee
# MAGIC GROUP BY 
# MAGIC     department_name
# MAGIC ORDER BY 
# MAGIC     total_salary DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     department_name, 
# MAGIC     country_name, 
# MAGIC     COUNT(employee_id) AS employee_count
# MAGIC FROM 
# MAGIC     Employee_info.fact_employee
# MAGIC GROUP BY 
# MAGIC     department_name, 
# MAGIC     country_name
# MAGIC ORDER BY 
# MAGIC     department_name, 
# MAGIC     country_name;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT 
# MAGIC     department_name, 
# MAGIC     country_name
# MAGIC FROM 
# MAGIC     Employee_info.fact_employee;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     department_name, 
# MAGIC     AVG(age) AS average_age
# MAGIC FROM 
# MAGIC     Employee_info.fact_employee
# MAGIC GROUP BY 
# MAGIC     department_name;
# MAGIC

# COMMAND ----------

# transformationi I would do on the fact data frame using data frame opertaion before writing to delta


dept_wise_salary_desc = joined_df.groupBy("Department") \
                     .agg(F.sum("Salary").alias("Total_Salary")) \
                     .orderBy(F.desc("Total_Salary"))

dept_wise_country_wise_emp_count = joined_df.groupby("Department", "Country")\
                      .agg(F.sum("EmployeeID").alias("emp_count"))\

department_country_df = joined_df.select("Department", "CountryName").distinct()

avg_age_dept_wise_df = joined_df.groupBy("Department")\
                        .agg(F.avg("Age").cast(IntegerType()).alias("avg_age"))

Department, Salary, EmployeeID, CountryName

department_country_df.show()