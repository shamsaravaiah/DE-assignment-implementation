# Databricks notebook source
storage_account_name = "salesviewadlsdev"
key = "hZNBlw9p9hcUbuNSzIHjPtM2by7KluxG4TaDhd7jAfFJj3O474JgupY82f9u7tLweuZ+rWC1wiHO+AStIX/epA=="

# Update the configuration to use wasbs instead of abfss
configs = {
  f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": key
}

container = "data-bricks-assignemnt-container"
dbutils.fs.mount(
  source = f"wasbs://{container}@{storage_account_name}.blob.core.windows.net/",
  mount_point = "/mnt/emp_mount",
  extra_configs = configs
)


# COMMAND ----------

