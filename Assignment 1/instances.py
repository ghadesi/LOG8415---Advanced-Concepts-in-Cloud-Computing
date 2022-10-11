def create_m4large_cluster(client, keyPair, securityGroup):
    print('Creating 5 instances of m4.large...')
    lowercase_a = 97
    ids = []
    
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
    print('Creating 4 instances of m4.large...')
    lowercase_a = 97
    ids = []

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


