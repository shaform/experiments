# install Java 8
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get install oracle-java8-set-default

# install Apache Spark
wget http://apache.stu.edu.tw/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz
tar -xzf spark-1.4.1-bin-hadoop2.6.tgz

# install sbt
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 642AC823
sudo apt-get update
sudo apt-get install sbt
