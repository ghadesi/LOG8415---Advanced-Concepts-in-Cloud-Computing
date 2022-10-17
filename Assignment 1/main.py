import time
import boto3
import requests
import threading
from datetime import datetime
from instances import *
from ELB import *
from analysis import *


def scenario1(elb_dns, path):
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)
        
        
def scenario2(elb_dns, path):
    for req in range(500):
        response = requests.get("http://" + elb_dns + path)
    time.sleep(60)
    for req in range(1000):
        response = requests.get("http://" + elb_dns + path)


def benchmark(elb_dns):
    # Cluster 1 benchmark
    now = datetime.now()
    print(str(now) + " --> Starting benchmark for cluster 1")
    thread1 = threading.Thread(target=scenario1, args=(elb_dns, "/cluster1",))
    thread2 = threading.Thread(target=scenario2, args=(elb_dns, "/cluster1",))
    
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
    thread1 = threading.Thread(target=scenario1, args=(elb_dns, "/cluster2",))
    thread2 = threading.Thread(target=scenario2, args=(elb_dns, "/cluster2",))

    now = datetime.now()
    print(str(now) + " --> Starting both threads for cluster 2")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    now = datetime.now()
    print(str(now) + " --> Ending benchmark for cluster 2")



def main():
    
    #initialise the attributs and clients that will be used
    #The follow 3 can change based on who wants to run (the access token is under me: Aleks)
    aws_access_key_id = 'ASIAQJSMAGZDQENEWDSC'
    secret_access_key = 'X7vpvIMF4TfQb0VEqyp327NZeNqI/6vbfpyahc7N'
    session_token = 'FwoGZXIvYXdzEEMaDHmkuDu2nuu9Wqy/NyLEAZHV0mp21d1TCdsICqtPsu2uRJEvEyHo6OGVmdWcz54KmXHo2HnZaUywhTzE/KVFUWBGA0k+0BYHU9iCz4Ti/o8OK51AmgsplfsTWp+16Ek/Tt2XCemlb1gqO//enJZB+W70pnpPkBkGZIi423n0DAkquncR8bczmTowEpZZ0Tvz7Q+80Wa5cFjMzPhhA/YKK6Xj1mt81oLvmorD8IvWiG3a9rcEWN9drPABPQv27Qo2ec93Z9BeH68D9GsNjKUklIa7glAowdSymgYyLctCqMOnM+TGRl0Q4Ko/wgxcIXMIpXxansEkF4rUcTaFRfH6jS26yq98B2eapg=='
    
    
    #Keypair for access and security group that needs to be assigned when instance is made (currently under me: Aleks)
    keyPairName = 'LOG8415E'
    securityGroup = 'LOG8415E security group'
    
    #EC2 client
    EC2 = boto3.client('ec2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
    region_name= 'us-east-1'
    )
    
    #Elastic Load Balancer client
    ELB = boto3.client('elbv2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
    region_name= 'us-east-1'
    )
    
    #Cloudwatch client
    CW = boto3.client('cloudwatch',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
    region_name= 'us-east-1'
    )
    
    #Create 5 m4.large instances
    m4Large_cluster_ids = create_m4large_cluster(EC2, keyPairName, securityGroup)
    #Create 4 t2.large instances
    t2Large_cluster_ids = create_t2large_cluster(EC2, keyPairName, securityGroup)
    
    print("Cluster1:")
    print(m4Large_cluster_ids)
    print("Cluster2:")
    print(t2Large_cluster_ids)
    
    # Give some breathing room for instances to initialise 
    print("Sleeping for 2 min for instances to initialise and set up flask")
    time.sleep(120)
    
    #get security group id
    sg_response = EC2.describe_security_groups(
    GroupNames=[securityGroup]
    )
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
    
    #get vpc_id
    vpc_id = EC2.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
    
    #create target groups for cluster 1 and cluster 2
    tg_cluster1, tg_cluster2 = create_target_groups(ELB, vpc_id)
    
    #create listener
    listener = create_elb_listener(ELB, tg_cluster1, load_balancer)
    
    #create rules for listener on cluster1 and cluster2
    create_rules(ELB, listener, tg_cluster1, tg_cluster2)
    
    #Register 5 m4.large instances to target group 1 and 4 t2.large instances to target group 2
    register_instances_to_target_groups(ELB, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2 )

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
        answer = input("- Enter 'terminate' to terminate the instance, elastic load balancer and target groups\n- Enter 'analysis' to pull metrics again\nChoice?:") 
        if answer == "terminate":
            #Destroy everything when user write 'yes'
            destructor(EC2, ELB, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2)
            destroy = True
        elif answer == 'analysis':
            analysis(CW, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)
        else: 
            continue 
            
    
    
def destructor(ec2_client, elb_client, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2):
            
    print("Deleting the load balancer (in the same time deleting the listener and rules)...")
    elb_client.delete_listener(ListenerArn=listener.get('Listeners')[0].get('ListenerArn'))
    
    time.sleep(20) 
    
    elb_client.delete_load_balancer(
        LoadBalancerArn = load_balancer.get('LoadBalancers')[0].get('LoadBalancerArn')
    )
    
    time.sleep(20) 
    
    #deregister the instances
    deregister_instances_from_target_groups(elb_client, m4Large_cluster_ids, t2Large_cluster_ids, tg_cluster1, tg_cluster2)
    
    time.sleep(10) 
    
    print("Deleting both target groups...")
    elb_client.delete_target_group(
        TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn')
    )
    elb_client.delete_target_group(
        TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn')
    )
    
    time.sleep(10) 
    
    print("Terminating instances...")
    terminate_instance_cluster(ec2_client, m4Large_cluster_ids)
    terminate_instance_cluster(ec2_client, t2Large_cluster_ids)
            

     
main()


