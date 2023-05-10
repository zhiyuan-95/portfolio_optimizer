from pyspark import SparkContext
import itertools

if __name__=='__main__':
    sc = SparkContext()
    rdd = sc.textFile('gs://bdma/data/weekly-patterns-nyc-2019-2020/part-*')
    header = rdd.first()
    rdd.sample(False, 0.01) \
        .coalesce(1) \
        .mapPartitions(lambda x: itertools.chain([header], x)) \
        .saveAsTextFile('gs://YOUR_BUCKET/weekly-patterns-nyc-2019-2020-sample')
