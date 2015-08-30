import org.apache.spark._
import org.apache.spark.rdd._
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

import org.apache.spark.mllib.feature.Word2Vec

object SparkW2V {
  def main(args: Array[String]) {
    val text8 = "{input directory}/text8"
    val output = "{output directory}/vectors.txt"
    val conf = new SparkConf().setAppName("Spark Word2Vec")
    val sc = new SparkContext(conf)

    val input = sc.textFile(text8).map(line => line.split(" ").toSeq)
    val word2vec = new Word2Vec()

    val model = word2vec.fit(input)
    model.save(sc, output)
  }
}
