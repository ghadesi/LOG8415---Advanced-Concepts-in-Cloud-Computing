import sys
from pyspark.sql import SparkSession

"""
Based on:
https://github.com/apache/spark/blob/master/examples/src/main/python/wordcount.py

"""


if len(sys.argv) != 2:
        print("Usage: sparkWordCount <file>", file=sys.stderr)
        sys.exit(-1)

spark = SparkSession.builder.master('local').appName('SparkWordCount').getOrCreate()
spark_context = spark.sparkContext

count = spark_context.textFile(sys.argv[1]).flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(lambda w, z:w +z).collect()

output = open('spark-output.txt', 'w+')
for (word, counter) in count:
        output.write("%s: %i" % (word, counter))

output.close()

spark.stop()
