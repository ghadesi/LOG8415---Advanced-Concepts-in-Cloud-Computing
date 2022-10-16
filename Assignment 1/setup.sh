#!/bin/bash
# Install necessary files and run Flask in the back ground 

sudo apt-get update &&
sudo pip3 install flask &&
sudo apt-get -y install python3-pip &&
mkdir flask_application && 
cd flask_application &&

instance_id=$(ec2metadata --instance-id) &&

echo "from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return \"Instance "$instance_id" is responding now! \"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)" | tee app.py &&
sudo python3 app.py
