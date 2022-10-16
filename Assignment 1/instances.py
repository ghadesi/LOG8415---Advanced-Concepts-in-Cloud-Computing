def testUserdata_create_m4large_cluster(client, keyPair, securityGroup):
    # I‌ create this function just for creating one instance and then check why user data not working
    # this a function for testing the user_data and it is temporary
    print('create one instance of m4.large...')
    lowercase_a = 97
    ids = []
    #USERDATA_SCRIPT = "#!/bin/bash \n sudo su \n yum update -y \n yum install -y httpd \n systemctl start httpd \n systemctl enable httpd \n "
    #here instead of flask I am installing apache 2 on the EC2 instance. I am providing -y option here to run this command silently
    USERDATA_SCRIPT = '''#!/bin/bash
    sudo apt update	
    sudo apt install apache2 -y
    apache2 -version
    sudo systemctl status apache2
    sudo echo “Hello World from $(hostname -f)” > /var/www/html/index.html'''
    
    #for main challenge here is that user data here is not wokring. I just create some variable and check the result for creating new instance to find the answer
    u_data = '''#!/bin/bash
        echo "Hello World" >> /tmp/data.txt'''

    u_data = '''
    # !/bin/bash
    echo
    'test' > / home / ec2 - user / test.txt
    '''
    # I‌ found that the main reason here for not running the flask in userdata is that the file does not save for each instance. I‌ mean when we create each instance and connect to
    # each instance I get that there is file named myap.py. I don't don't knwo why but I‌ found a solution to run our simple server file without create a new file.
    
    sudo echo -e "from flask import Flask\napp = Flask(__name__)\n@app.route('/')\ndef hello():return 'VM name:'\nif __name__ == '__main__':app.run(host='0.0.0.0', port=80, debug=False)"| python3 
    instance = 0
    response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdf',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'gp2',
                    },
                },
            ],
            ImageId='ami-08c40ec9ead489470',
            InstanceType='m4.large',
            KeyName=keyPair,
            UserData=USERDATA_SCRIPT,
            Placement={
                'AvailabilityZone': 'us-east-1' + chr(lowercase_a + instance),
            },
            SecurityGroups=[
                securityGroup,
            ],
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'name',
                            'Value': 'cluster1'
                        },
                    ]
                },
            ],
        )
    ids.append(response["Instances"][0]["InstanceId"])
    return ids

  
    # Here we create 4 instances for target group2. For creating a new instance we use "run_instances" function. There are some parameters we can fix there.
    # This example sets the EBS-backed root device (/dev/sdf) size to 8 GiB.
    # InstanceType define the instance type.
    # in Placement we set the AvailabilityZone. As mention in the asignment we need to have diffrent AvailabilityZone for each instanec in target group.
  
def create_m4large_cluster(client, keyPair, securityGroup):
    print('Creating 5 instances of m4.large...')
    lowercase_a = 97
    ids = []
    
    USERDATA_SCRIPT = '''#!/bin/bash \n mkdir Aleks \n
    # Install necessary files and run Flask in the back ground 

    sudo apt update
    mkdir flask_application && cd flask_application
    sudo apt install python3-pip python3-flask -y

    INSTANCE_NAME=$(ec2metadata --instance-id)

    echo "from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    def hello():
        return 'VM name: $INSTANCE_NAME'
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)" > my_app.py

    nohup sudo python3 my_app.py &
    '''
    
    for instance in range(5):
        response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdf',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'gp2',
                    },
                },
            ],
            ImageId='ami-08c40ec9ead489470',
            InstanceType='m4.large',
            KeyName=keyPair,
            UserData=USERDATA_SCRIPT,
            Placement={
                'AvailabilityZone': 'us-east-1'+chr(lowercase_a + instance),
            },
            SecurityGroups=[
                securityGroup,
            ],
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'name',
                            'Value': 'cluster1'
                        },
                    ]
                },
            ],
        )
        ids.append(response["Instances"][0]["InstanceId"])
        
    return ids


    # Here we create 4 instances for target group2. For creating a new instance we use "run_instances" function. There are some parameters we can fix there.
    # This example sets the EBS-backed root device (/dev/sdf) size to 8 GiB.
    # InstanceType define the instance type.
    # in Placement we set the AvailabilityZone. As mention in the asignment we need to have diffrent AvailabilityZone for each instanec in target group.
  
def create_t2large_cluster(client, keyPair, securityGroup):
    print('Creating 4 instances of t2.large...')
    lowercase_a = 97
    ids = []
    
    #This is for user_data. when a instance is created we can run a script to run after the instance is created. it can be anything from updating the operating
    # system to install flask or apache server
    # in this script we try to install a simple flask server to show the instance id from port 80
    USERDATA_SCRIPT = '''#!/bin/bash \n mkdir Aleks \n
    # Install necessary files and run Flask in the back ground 

    sudo apt update
    mkdir flask_application && cd flask_application
    sudo apt install python3-pip python3-flask -y

    INSTANCE_NAME=$(ec2metadata --instance-id)

    echo "from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    def hello():
        return 'VM name: $INSTANCE_NAME'
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)" > my_app.py

    nohup sudo python3 my_app.py &
    '''
    # Here we create 4 instances for target group2. For creating a new instance we use "run_instances" function. There are some parameters we can fix there.
    # This example sets the EBS-backed root device (/dev/sdf) size to 8 GiB.
    # InstanceType define the instance type.
    # in Placement we set the AvailabilityZone. As mention in the asignment we need to have diffrent AvailabilityZone for each instanec in target group.
    for instance in range(4):
        response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdf',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 8,
                        'VolumeType': 'gp2',
                    },
                },
            ],
            ImageId='ami-08c40ec9ead489470',
            InstanceType='t2.large',
            KeyName=keyPair,
            UserData=USERDATA_SCRIPT,
            Placement={
                'AvailabilityZone': 'us-east-1'+chr(lowercase_a + instance),
            },
            SecurityGroups=[
                securityGroup,
            ],
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'name',
                            'Value': 'cluster2'
                        },
                    ]
                },
            ],
        )
        ids.append(response["Instances"][0]["InstanceId"])
        
    return ids

# This function is defined to terminate the instances by function "terminate_instances".
def terminate_instance_cluster(client, instanceIds):
    print('terminating cluster of instances:')
    print(instanceIds)
    client.terminate_instances(InstanceIds=(instanceIds))


