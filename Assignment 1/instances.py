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


def create_t2large_cluster(client, keyPair, securityGroup):
    print('Creating 4 instances of t2.large...')
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


def terminate_instance_cluster(client, instanceIds):
    print('terminating cluster of instances:')
    print(instanceIds)
    client.terminate_instances(InstanceIds=(instanceIds))


