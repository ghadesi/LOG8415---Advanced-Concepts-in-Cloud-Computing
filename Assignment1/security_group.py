

def create_security_group(ec2_client, sg_name, vpc_id):
    """
    Function that creates security group and assigns inbound rules

    :param ec2_client: The ec2 client that creates the security group
    :param sg_name: The name of the security group
    :param vpc_id: id of the vpc need to create security group

    :returns: the created security group
    """
    security_group = ec2_client.create_security_group(
        Description="TP1 Security Group",
        GroupName=sg_name,
        VpcId=vpc_id
    )
    add_inbound_rules(ec2_client, security_group['GroupId'])
    return security_group



def add_inbound_rules(ec2_client, sg_id):
    """
    Function that assigns inbound rules to the security group

    :param ec2_client: The ec2 client that will assign rules
    :param sg_id: Security group's id
    """

    inbound_rules = [
        {
            'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
        ]
    ec2_client.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=inbound_rules)



def delete_security_group(ec2_client, sg_id):
    """
    Function that deletes  the security group

    :param ec2_client: The ec2 client that will delete in teardown
    :param sg_id: Security group's id
    """
    ec2_client.delete_security_group(GroupId=sg_id)