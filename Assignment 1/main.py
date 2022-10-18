import time
import boto3
import requests
import threading
from datetime import datetime
from instances import *
from security_group import *
from key_pair import *
from ELB import *
from analysis import *
import os
from dotenv import load_dotenv

load_dotenv("./credentials")


def scenario1(elb_dns, path):
    """
    Function that does 1000 requests

    :param elb_dns: dns of the ELB
    :param path: path to specify --> /cluster1 or /cluster2
    """
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)


def scenario2(elb_dns, path):
    """
    Function that does 500 requests, break of 1min, then 1000 requests

    :param elb_dns: dns of the ELB
    :param path: path to specify --> /cluster1 or /cluster2
    """
    for req in range(500):
        response = requests.get("http://" + elb_dns + path)
    time.sleep(60)
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)


def benchmark(elb_dns):
    """
    Function that commits the benchmark

    :param elb_dns: dns of the ELB
    """
    # Cluster 1 benchmark
    now = datetime.now()
    print(str(now) + " --> Starting benchmark for cluster 1")
    thread1 = threading.Thread(target=scenario1, args=(
        elb_dns,
        "/cluster1",
    ))
    thread2 = threading.Thread(target=scenario2, args=(
        elb_dns,
        "/cluster1",
    ))

    now = datetime.now()
    print(str(now) + " --> Starting both threads for cluster 1")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    now = datetime.now()
    print(str(now) + " --> Ending benchmark for cluster 1")

    # Cluster 2 benchmark
    now = datetime.now()
    print(str(now) + " --> Starting benchmark for cluster 2")
    thread1 = threading.Thread(target=scenario1, args=(
        elb_dns,
        "/cluster2",
    ))
    thread2 = threading.Thread(target=scenario2, args=(
        elb_dns,
        "/cluster2",
    ))

    now = datetime.now()
    print(str(now) + " --> Starting both threads for cluster 2")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    now = datetime.now()
    print(str(now) + " --> Ending benchmark for cluster 2")


def main():
    """
    Main function of the assignement
    """
    aws_access_key_id = os.environ["aws_access_key_id"]
    aws_secret_access_key = os.environ["aws_secret_access_key"]
    aws_session_token = os.environ["aws_session_token"]

    #Keypair for access and security group that needs to be assigned when instance is made
    keyPairName = 'LOG8415E'
    securityGroupName = 'LOG8415E security group'

    #EC2 client
    EC2 = boto3.client(
        'ec2',
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

    #Elastic Load Balancer client
    ELB = boto3.client(
        'elbv2',
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

    #Cloudwatch client
    CW = boto3.client(
        'cloudwatch',
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

    #get vpc_id
    vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')

    print('Creating key pair...')
    create_key_pair(EC2, keyPairName)
    print('Creating security group...')
    create_security_group(EC2, securityGroupName, vpc_id)

    #Create 5 m4.large instances
    m4Large_cluster_ids = create_m4large_cluster(EC2, keyPairName, securityGroupName)
    #Create 4 t2.large instances
    t2Large_cluster_ids = create_t2large_cluster(EC2, keyPairName, securityGroupName)

    print("Cluster1:")
    print(m4Large_cluster_ids)
    print("Cluster2:")
    print(t2Large_cluster_ids)

    # Give some breathing room for instances to initialise
    print("Sleeping for 2 min for instances to initialise and set up flask")
    time.sleep(120)

    #get security group id
    sg_response = EC2.describe_security_groups(GroupNames=[securityGroupName])
    sg_id = sg_response.get('SecurityGroups')[0].get('GroupId')

    #get subnets from availability zone a to e
    all_subnets = EC2.describe_subnets()
    subnets = []
    five_zones = ['us-east-1a', 'us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e']
    for subnet in all_subnets['Subnets']:
        if subnet['AvailabilityZone'] in five_zones:
            subnets.append(subnet['SubnetId'])

    #Create ELB
    load_balancer = create_load_balancer(ELB, subnets, sg_id)
    ELB_DNS = str(load_balancer.get('LoadBalancers')[0].get('DNSName'))
    print("ELB was created. DNS: " + ELB_DNS)

    #create target groups for cluster 1 and cluster 2
    tg_cluster1, tg_cluster2 = create_target_groups(ELB, vpc_id)

    #create listener
    listener = create_elb_listener(ELB, tg_cluster1, load_balancer)

    #create rules for listener on cluster1 and cluster2
    create_rules(ELB, listener, tg_cluster1, tg_cluster2)

    #Register 5 m4.large instances to target group 1 and 4 t2.large instances to target group 2
    register_instances_to_target_groups(ELB, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)

    print("Give 3 min for ELB to get active")
    time.sleep(180)

    #Benchmark
    benchmark(ELB_DNS)

    print("Take a 1 min breather post-requests before doing the analysis...")
    time.sleep(60)

    #cloudwatch metrics analysis
    print("Running analysis...")
    analysis(CW, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)

    destroy = False
    while destroy == False:
        answer = input(
            "- Enter 'terminate' to terminate the instance, elastic load balancer and target groups\n- Enter 'analysis' to pull metrics again\nChoice?:"
        )
        if answer == "terminate":
            #Destroy everything when user write 'yes'
            destructor(EC2, ELB, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2, sg_id, keyPairName)
            destroy = True
        elif answer == 'analysis':
            analysis(CW, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)
        else:
            continue


def destructor(
    ec2_client, elb_client, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2, security_group, keyPair
):
    """
    Function that does the teardown of instances, ELB, target groups etc...

    :param ec2_client: client of ec2
    :param elb_client: elb client
    :param m4Large_cluster_ids: IDs of m4.large instances
    :param t2Large_cluster_ids: IDs of t2.large instances
    :param load_balancer: load balancer
    :param listener: the listener to the load balancer
    :param tg_cluster1: the target group for cluster 1
    :param tg_cluster2: the target group for cluster 3
    :param security_group: ID of security group 1
    :param keyPair: Name of key pair
    """

    print("Deleting the load balancer (in the same time deleting the listener and rules)...")
    elb_client.delete_listener(ListenerArn=listener.get('Listeners')[0].get('ListenerArn'))

    time.sleep(20)

    elb_client.delete_load_balancer(LoadBalancerArn=load_balancer.get('LoadBalancers')[0].get('LoadBalancerArn'))

    time.sleep(20)

    #deregister the instances
    deregister_instances_from_target_groups(elb_client, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)

    time.sleep(10)

    print("Deleting both target groups...")
    elb_client.delete_target_group(TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'))
    elb_client.delete_target_group(TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'))

    time.sleep(10)

    print("Terminating instances...")
    terminate_instance_cluster(ec2_client, m4Large_cluster_ids)
    terminate_instance_cluster(ec2_client, t2Large_cluster_ids)

    print("Giving 3 min to make sure all instances are terminated so we can delete security group without dependency")
    time.sleep(180)
    print("Deleting keypair and security group")
    delete_security_group(ec2_client, security_group)
    time.sleep(10)
    delete_key_pair(ec2_client, keyPair)


main()
