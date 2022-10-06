#!/bin/bash
# Install necessary files and run Flask in the back ground 

sudo apt update
mkdir flask_application && cd flask_application
sudo apt install python3-pip python3-flask -y

INSTANCE_NAME='Amin'

echo "from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'VM name: $INSTANCE_NAME'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)" > my_app.py

nohup sudo python3 my_app.py &
