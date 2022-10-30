def create_key_pair(ec2_client, keypair_name):
    """
    Make key pair to be able to connect to instances

    :param ec2_client: The ec2 client that creates the key pair
    :param keypair_name: The name of the key pair

    :returns: The key pair's name
    """
    key_pair = ec2_client.create_key_pair(
    KeyName=keypair_name,
    KeyType='rsa',
    KeyFormat='pem'
    )
    return key_pair['KeyName']


def delete_key_pair(ec2_client, key_pair):
    """
    Function that will delete key pair in the teardown

    :param ec2_client: The ec2 client that deletes the key pair
    :param key_pair: The name of the key pair
    """
    ec2_client.delete_key_pair(KeyName=key_pair)