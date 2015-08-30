cd sparkw2v
sbt package

cd ..
spark-1.4.1-bin-hadoop2.6/bin/spark-submit --class SparkW2V --master local[*] --executor-memory 20G --driver-memory 10G sparkw2v/target/scala-2.10/spark-word2vec_2.10-1.0.jar
