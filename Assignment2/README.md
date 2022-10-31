# Assignement 2 (Azure)

We did this assignement on an Azure Ubuntu VM

## Setup

Once in the Azure VM terminal, make sure you are in the user's home directory. By the below command you change your directory to the home directory.
```bash
user@localhost: cd ~
```

By switching to the root privilege mode, we don't need to sudo all the time and no permissions problem. 
```bash
sudo su
```

Go back to the root's home directory.
```bash
root@localhost: cd ~
```

Install latest Azure VM updates and java.
```bash
apt-get update
apt install default-jre -y
apt install default-jdk -y
```

To add the variables related to the JAVA packages, we append following lines at the end of the ```.profile``` file and reconfigure the bash variables. 
```bash
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.profile
echo "export PATH=$JAVA_HOME/bin" >> ~/.profile
source ~/.profile
```

Next, get hadoop tar, decompress it and move it to a ```usr/local/hadoop``` folder.

```bash
wget "https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz"
tar -xf hadoop-3.3.4.tar.gz  -C /usr/local/
mv /usr/local/hadoop-* /usr/local/hadoop
```

To add the variables related to the Hadoop package, we append following lines at the end of the ```.profile``` file and reconfigure the bash variables. 
```bash
echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.profile
echo "export PATH=$PATH:$HADOOP_HOME/bin" >> ~/.profile
echo "export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop" >> ~/.profile
source ~/.profile
```

Define following parameters in the ```etc/hadoop/hadoop-env.sh``` file.
```bash
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo "export HADOOP_PREFIX=/usr/local/hadoop" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
source /usr/local/hadoop/etc/hadoop/hadoop-env.sh
```

Try to type ```hadoop``` in terminal. If you don't get hadoop menu, then extend the PATH variable.
```bash
export PATH=$PATH:/usr/local/hadoop/bin/
```

## Running Hadoop
We have based our WordCount.java on these websites: [apache.org](<http://svn.apache.org/viewvc/hadoop/common/trunk/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples/WordCount.java?view=log>) and [stackoverflow.com](<https://stackoverflow.com/questions/26700910/hadoop-java-error-exception-in-thread-main-java-lang-noclassdeffounderror-w>)


First, we want to make sure that ```WordCount.java``` and the dataset folder that contains ```pg4300.txt``` and the 9 target datasets from our github on the root's home directory. Then build ```WordCount.java```.
```bash
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
```
Here is an example of command:
```bash
time hadoop jar wc.jar WordCount dataset/pg4300.txt output
```
> The time command is used to determine how long a given command takes to run. It is useful for testing the performance of our scripts and commands.

## Running Linux command

First, make sure you have the dataset folder from our github on the root's home directory.
```bash
root@localhost: cd ~
```

Compute the word frequency of a text with Linux, using Linux commands and pipes, as follows:
```bash
time cat dataset/pg4300.txt | tr ' ' '\n' | sort | uniq -c >> output.txt
```
We use ```>> output.txt``` so the output is put in a text file instead of saturating the terminal. If you want to check results, you can ```nano``` into it.

## Running Spark
We have based our sparkWordCount.py from this [link](<https://github.com/apache/spark/blob/master/examples/src/main/python/wordcount.py>).

Again, make sure you have ```sparkWordCount.py``` and the dataset folder from our github on the root's home directory.

Get the spark dependencies.
```bash
apt-get update
apt-get install python3-pip 
pip install pyspark
```

Example of spark command:
```bash
time spark-submit sparkWordCount.py dataset/buchanj-midwinter-00-t.txt
```

If you get something like spark-submit command not found, you can also do:
```bash
 time /usr/local/bin/spark-submit sparkWordCount.py dataset/buchanj-midwinter-00-t.txt
```

## Running mapper and reducer for “People You Might Know"
Make sure you have mapper.py, reducer.py and soc-LiveJournal1Adj.txt from our github on the root's home directory.

Install python 2.7, because our mapper and reducer have ```#!/usr/bin/env python```
```bash
apt-get install python
```

Here is the command to run
```bash
hadoop jar  /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar  -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input soc-LiveJournal1Adj.txt -output output
```
If you get an error like ```‘python3\r’: No such file or directory```, then it means the formatting of the mapper and reducer are Windows/DOS-style instead of Linux style

There is two options to fix it...

### Option 1:
You install dos2unix
```bash
apt install dos2unix
```

And convert the mapper and reducer to unix with a command like this.
```bash
dos2unix mapper_OR_reducer.py
```

### Option 2:
The second option is to simply deleting the mapper.py and reducer.py that are in the home directory.
```bash
rm -r mapper.py
rm -r reducer.py
```

Touch them
```bash
touch mapper.py
touch reducer.py 
```

Nano mapper.py and copy-paste its respective code into it
```bash
nano mapper.py
```

Nano reducer.py and copy-paste its respective code into it
```bash
nano reducer.py 
```
