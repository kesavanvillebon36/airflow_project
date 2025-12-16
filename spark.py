
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Datacamp Pyspark Tutorial").config("spark.memory.offHeap.enabled","true").config("spark.memory.offHeap.size","10g").getOrCreate()

path = "examples/src/main/resources/people.json"
path = "home/kesav/airflowtuto/demofile.json"
peopleDF = spark.read.json(path)