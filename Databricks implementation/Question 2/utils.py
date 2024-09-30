# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from datetime import datetime

def add_date_column(df):
  current_date = datetime.now().date()
  temp_df = df.withColumn("load_date", lit(current_date))
  return temp_df
