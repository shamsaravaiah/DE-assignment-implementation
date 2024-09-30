# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql import Row

# Create a SparkSession
spark = SparkSession.builder \
    .appName("CreateDataFrameExample") \
    .getOrCreate()

# Sample data
data = [("John", 25), ("Alice", 30), ("Bob", 35)]

# Define the schema
schema = ["name", "age"]

# Create RDD from data
rdd = spark.sparkContext.parallelize(data)

# Convert RDD to DataFrame
df = rdd.map(lambda x: Row(name=x[0], age=int(x[1]))).toDF(schema)

# Show the DataFrame
df.show()

# Stop the SparkSession
spark.stop()
