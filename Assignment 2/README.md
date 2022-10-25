#This a summary for What We have done during the assigment.

Hadoop tutorial: http://dzone.com/articles/getting-hadoop-and-running.

Java install on ubuntu: [https://ubuntuhandbook.org/index.php/2014/02/install-oracle-java-6-7-or-8-ubuntu-14-04/](https://linuxhint.com/install-java-ubuntu-22-04/)

```bash
Javac
java -version
```
In case you have not already installed Java:



```bash
sudo apt-get update
sudo apt install -y openjdk-18-jdk
sudo apt install -y openjdk-18-jre
```

Once Java is installed, you should set JAVA_HOME/bin to your PATH, to ensure java is available from the command line. Profile is run once when we run our instance.
```bash
nano ~/.profile  
```
Append following lines to it and save.

```bash
export JAVA_HOME=/usr/lib/jvm/java-18-oracle
export PATH=$JAVA_HOME/bin 
```


Note that after editing, you should re-login in order to initialize the variables, but you could use following command and use the variable without re-login.

```bash
source ~/.profile 
```

or instead of open profile and add these line just type this command: 

```bash
sudo echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" >> ~/.profile
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
```
Then open profile and Append following lines to it and save.


```bash
echo "export HADOOP_PREFIX=/usr/local/hadoop-3.3.4" >> ~/.profile
echo "export PATH=$HADOOP_PREFIX/bin:$PATH" >> ~/.profile
source ~/.profile
```
Define following parameters in etc/hadoop/hadoop-env.sh file.

```bash
echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 /usr/local/hadoop-3.3.4/etc/hadoop/hadoop-env.sh"
echo "export HADOOP_PREFIX=/usr/local/hadoop-3.3.4 /usr/local/hadoop-3.3.4/etc/hadoop/hadoop-env.sh"
source /usr/local/hadoop-3.3.4/etc/hadoop/hadoop-env.sh
```

```bash

```

