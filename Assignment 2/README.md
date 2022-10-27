# This a summary for What We have done during the assigment.

Hadoop tutorial: http://dzone.com/articles/getting-hadoop-and-running.

Java install on ubuntu:


```bash
Javac
java -version
```
In case you have not already installed Java:

```bash
sudo apt-get update
sudo apt install default-jre -y
sudo apt install default-jdk -y
```
Now check java version. in my case following this photo my java version is 11.So from now on everywhere you see java-11 you can repalce ir with your java version.

![java version](https://user-images.githubusercontent.com/80580733/197911176-e3d57be0-6cc8-4878-a1f5-cffe99f8d5e5.png)


Once Java is installed, you should set JAVA_HOME/bin to your PATH, to ensure java is available from the command line. Profile is run once when we run our instance.
```bash
nano ~/.profile  
```
Append following lines to it and save.

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin 
```


Note that after editing, you should re-login in order to initialize the variables, but you could use following command and use the variable without re-login.

```bash
source ~/.profile 
```

or instead of open profile and add these line just type this command: 

```bash
sudo echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.profile
sudo echo "export PATH=$JAVA_HOME/bin" >> ~/.profile
source ~/.profile
```

Check the value of JAVA_HOME directory:

```bash
echo $JAVA_HOME
```

If you get error like "The command could not be located because '/bin:/usr/bin' is not included in the PATH environment variable." run this command to fix it.

```bash
export PATH="/usr/bin:$PATH"
```


I found the last hadoop version from thin link:  then download it.

The source prefer Hadoop being installed in /usr/local directory (I don't know why!). Decompress the downloaded file using the following command.

```bash
sudo wget "https://dlcdn.apache.org/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz"
sudo tar -xf hadoop-3.3.4.tar.gz  -C /usr/local/
sudo mv /usr/local/hadoop-* /usr/local/hadoop
```
Then open profile and Append following lines to it and save.

```bash
echo "export HADOOP_HOME=/usr/local/hadoop" >> ~/.profile
echo "export PATH=$PATH:$HADOOP_HOME/bin" >> ~/.profile
echo "export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop" >> ~/.profile
source ~/.profile
```

Finally these line should be added to profile
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
#export JAVA_HOME=/usr/lib/jvm/java-11-oracle
export PATH=$PATH:$JAVA_HOME/bin 
export HADOOP_HOME=/usr/local/hadoop/
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
```

Define following parameters in etc/hadoop/hadoop-env.sh file.

```bash
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
echo "export HADOOP_PREFIX=/usr/local/hadoop" >> /usr/local/hadoo/etc/hadoop/hadoop-env.sh
source /usr/local/hadoop/etc/hadoop/hadoop-env.sh
```

 <!--- 
I get the word count from here: https://www.dropbox.com/s/yp9i7nwmgzr3nkx/WordCount.java?dl=0

```bash
mkdir example && cd example
touch WordCount.java
mkdir input_data && cd input_data
touch input.txt
```

# Install SSH

```bash
apt-get install ssh -y

```

```bash
cd /usr/local/hadoop/etc/hadoop
sudo nano nano core-site.xml

<configuration>
  <property>
      <name>fs.defaultFS</name>
      <value>hdfs://ec2-44-200-190-242.compute-1.amazonaws.com:9000</value>
    </property>
</configuration>

```

```bash
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar grep input output 'dfs[a-z.]+'

hadoop jar /home/cloudera/WordCount.jar WordCount /inputnew/inputfile.txt /outputnew

```
# Hadoop HDFS
---> 


# Experiments with WordCount

Hadoop comes with a set of demonstration programs. One of them is WordCount.java which will
automatically compute the word frequency of all text files found in the HDFS directory you ask it to process.

We create a Worcount.java file with our desire algorithm. 

```bash
nano WordCount.java
```
Then We Compile WordCount.java and create a jar:

```bash
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
```
Create a sample input file in a folder name input.txt

```bash
hadoop fs -ls /usr/local/hadoop/myexample/input
#Found 1 items
#-rw-r--r--   1 root root         62 2022-10-26 05:01 /usr/local/hadoop/myexample/input/input.txt
```
Then run it: 

```bash
hadoop jar wc.jar WordCount /usr/local/hadoop/myexample/input /usr/local/hadoop/myexample/output
```
See the Output: 

```bash
hadoop fs -cat /usr/local/hadoop/myexample/output/part-00000 
```


I get word count from here: http://svn.apache.org/viewvc/hadoop/common/trunk/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples/WordCount.java?view=log


```bash
time hadoop jar wc.jar WordCount dataset/pg4300.txt output3
time cat pg4300.txt | tr '[:space:]' '[\n*]' | grep -v "^\s*$" | sort | uniq -c 
```

```bash
hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar -input myinput -output myoutput -mapper /home/expert/hadoop-1.2.1/mapper.py -reducer /home/expert/hadoop-1.2.1/reducer.py```



