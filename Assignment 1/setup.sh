#!/bin/bash

apt update;
apt -y install python3-pip;
pip3 install flask;

instance_id=$(ec2metadata --instance-id);

python3 -c "
from flask import Flask

app = Flask(__name__)

@app.route('/')
def default_route():
    return 'Instance "$instance_id" is responding now! '

@app.route('/cluster1')
def cluster1_route():
    return 'Instance "$instance_id" is responding now from target group cluster1 ! '

@app.route('/cluster2')
def cluster2_route():
    return 'Instance "$instance_id" is responding now from target group cluster2 ! '

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
";
