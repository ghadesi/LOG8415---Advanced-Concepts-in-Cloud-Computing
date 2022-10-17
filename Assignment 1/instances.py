
    # Here we create 5 instances for target group2. For creating a new instance we use "run_instances" function. There are some parameters we can fix there.
    # This example sets the EBS-backed root device (/dev/sda1) size to 8 GiB.
    # InstanceType define the instance type.
    # in Placement we set the AvailabilityZone. As mention in the asignment we need to have diffrent AvailabilityZone for each instance in target group.
  
def create_m4large_cluster(client, keyPair, securityGroup):
    print('Creating 5 instances of m4.large...')
    lowercase_a = 97
    ids = []
    
    for instance in range(5):
        response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
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
            UserData=open('setup.sh').read(),
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
                            'Key': 'Name',
                            'Value': 'cluster1' + chr(lowercase_a + instance)
                        },
                    ]
                },
            ],
        )
        ids.append(response["Instances"][0]["InstanceId"])
        
    return ids


    # Here we create 4 instances for target group2. For creating a new instance we use "run_instances" function. There are some parameters we can fix there.
    # This example sets the EBS-backed root device (/dev/sda1) size to 8 GiB.
    # InstanceType define the instance type.
    # in Placement we set the AvailabilityZone. As mention in the asignment we need to have diffrent AvailabilityZone for each instance in target group.
  
def create_t2large_cluster(client, keyPair, securityGroup):
    print('Creating 4 instances of t2.large...')
    lowercase_a = 97
    ids = []

    for instance in range(4):
        response = client.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
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
            UserData=open('setup.sh').read(),
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
                            'Key': 'Name',
                            'Value': 'cluster2' + chr(lowercase_a + instance)
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


