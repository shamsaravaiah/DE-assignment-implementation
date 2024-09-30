# Databricks notebook source
storage_account_name = "salesviewadlsdev"
key = "hZNBlw9p9hcUbuNSzIHjPtM2by7KluxG4TaDhd7jAfFJj3O474JgupY82f9u7tLweuZ+rWC1wiHO+AStIX/epA=="

# Update the configuration to use wasbs instead of abfss
configs = {
  f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": key
}

container = "bronze"
dbutils.fs.mount(
  source = f"wasbs://{container}@{storage_account_name}.blob.core.windows.net/",
  mount_point = "/mnt/bronze",
  extra_configs = configs
)


# COMMAND ----------

storage_account_name = "salesviewadlsdev"
key = "hZNBlw9p9hcUbuNSzIHjPtM2by7KluxG4TaDhd7jAfFJj3O474JgupY82f9u7tLweuZ+rWC1wiHO+AStIX/epA=="

# Update the configuration to use wasbs instead of abfss
configs = {
  f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": key
}

container = "silver"
dbutils.fs.mount(
  source = f"wasbs://{container}@{storage_account_name}.blob.core.windows.net/",
  mount_point = "/mnt/silver",
  extra_configs = configs
)


# COMMAND ----------

storage_account_name = "salesviewadlsdev"
key = "hZNBlw9p9hcUbuNSzIHjPtM2by7KluxG4TaDhd7jAfFJj3O474JgupY82f9u7tLweuZ+rWC1wiHO+AStIX/epA=="

# Update the configuration to use wasbs instead of abfss
configs = {
  f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": key
}

container = "gold"
dbutils.fs.mount(
  source = f"wasbs://{container}@{storage_account_name}.blob.core.windows.net/",
  mount_point = "/mnt/gold",
  extra_configs = configs
)
