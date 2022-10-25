#This a summary for What We have done during the assigment.

Hadoop tutorial: http://dzone.com/articles/getting-hadoop-and-running.

Java install on ubuntu: [https://ubuntuhandbook.org/index.php/2014/02/install-oracle-java-6-7-or-8-ubuntu-14-04/](https://linuxhint.com/install-java-ubuntu-22-04/)

```bash
Javac
java -version
```
In case you have not already installed Java:

```bash

```

```bash
sudo apt-get update
sudo apt install -y openjdk-18-jdk
sudo apt install -y openjdk-18-jre
```

Once Java is installed, you should set JAVA_HOME/bin to your PATH, to ensure java is available from the command line.
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
