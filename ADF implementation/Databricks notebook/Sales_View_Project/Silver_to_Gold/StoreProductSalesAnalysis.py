# Databricks notebook source
# MAGIC %run "/Workspace/Sales_View_Project/Silver_to_Gold/utils"

# COMMAND ----------

from pyspark.sql.functions import col


# COMMAND ----------

product_path = "/mnt/silver/sales_view/product"
store_path = "/mnt/silver/sales_view/store"
store_df = read_delta_table(store_path)
product_df = read_delta_table(product_path)

store_df.display()
product_df.display()

# COMMAND ----------

product_store_df = store_df.join(product_df, store_df.store_id == product_df.store_id, "inner")
product_store_df.display()

# COMMAND ----------

customer_sales_df = read_delta_table("/mnt/silver/sales_view/customer_sales")
customer_sales_df.display()


# COMMAND ----------


customer_sales_df_alias = customer_sales_df.alias("cs")
product_store_df_alias = product_store_df.alias("ps")

final_gold_df = customer_sales_df_alias.join(product_store_df_alias, col("cs.product_id") == col("ps.product_id"), "inner") 

# Select the columns you want, specifying the product_id from one DataFrame to resolve ambiguity
final_gold_df = final_gold_df.select(
    "cs.order_date",       # order_date from customer_sales_df
    "cs.category",         # category from customer_sales_df
    "cs.city",             # city from customer_sales_df
    "cs.customer_id",      # customer_id from customer_sales_df
    "cs.product_id",       # product_id from customer_sales_df (resolved ambiguity)
    "cs.profit",           # profit from customer_sales_df
    "cs.region",           # region from customer_sales_df
    "cs.sales",            # sales from customer_sales_df
    "cs.segment",          # segment from customer_sales_df
    "cs.ship_date",        # ship_date from customer_sales_df
    "cs.ship_mode",        # ship_mode from customer_sales_df
    "cs.latitude",         # latitude from customer_sales_df
    "cs.longitude",        # longitude from customer_sales_df
    "ps.store_name",       # store_name from product_store_df
    "ps.location",         # location from product_store_df
    "ps.manager_name",     # manager_name from product_store_df
    "ps.product_name",     # product_name from product_store_df
    "ps.price",            # price from product_store_df
    "ps.stock_quantity",   # stock_quantity from product_store_df
    "ps.image_url"         # image_url from product_store_df
)



# COMMAND ----------

final_gold_df.display()

# COMMAND ----------

product_store_df = store_df.alias("s").join(product_df.alias("p"), "store_id", "inner")

desired_columns = [
    "s.store_id",
    "s.store_name",
    "s.location",
    "s.manager_name",
    "p.product_name",
    "p.product_code",
    "p.description",
    "p.category_id",
    "p.price",
    "p.stock_quantity",
    "p.supplier_id",
    "p.created_at",
    "p.updated_at",
    "p.image_url",
    "p.weight",
    "p.expiry_date",
    "p.is_active",
    "p.tax_rate"
]

product_store_df = product_store_df.select(*desired_columns)
product_store_df.display()



# COMMAND ----------

final_gold_df.write.format("delta").mode("overwrite").save("/mnt/gold/sales_view/StoreProductSalesAnalysis")
