import time
import boto3
from instances import *
from ELB import *


def main():
    
    #initialise the attributs and clients that will be used
    #The follow 3 can change based on who wants to run (the access token is under me: Aleks)
    aws_access_key_id = 'ASIAQJSMAGZDYUYHJGVO'
    secret_access_key = 'IPHMQaRivxClUMXsoPS3X3/ZEsG5t91m8DNavPU7'
    session_token = 'FwoGZXIvYXdzEML//////////wEaDCIQ/10Lk/+sS0mlKyLEAW+O9tsOSwNlOBgTGJxBCDmVR+h9UiIx4p2/Zo76EOH7dIgXrQ5XdQjbwWRFF1r/VQaYQ3i57ZRuLZ6y9fpJfOVFMA7JijyrSDwV9BHEAzmFIJFXe+4RBDey8cQglb1rJgTEjBmBAbYvvS7xTcvVCe9I2e1/rHG8VpIrnx9ETLw9uDkSXtOpcDtPbpiLYj2js7i3lgRGL6mGucUnDRbPgJRxNjlkKzBDm9EL2Aw371p0Qb9kl/Bp42HqK3YkZ3+ipMG90e8ow8KWmgYyLYhHM6uEfdQ1Ha+LIRvTUGIufr4NYRsRSbV4MjDL25DFjYBS43pCuAku8cX20w=='
    
    
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
    
    #Create 5 m4.large instances
    m4Large_cluster_ids = create_m4large_cluster(EC2, keyPairName, securityGroup)
    #Create 4 t2.large instances
    t2Large_cluster_ids = create_t2large_cluster(EC2, keyPairName, securityGroup)
    
    print("Cluster1:")
    print(m4Large_cluster_ids)
    print("Cluster2:")
    print(t2Large_cluster_ids)
    
    # Give some breathing room for instances to initialise 
    print("Sleeping for 60 sec for instances to initialise")
    time.sleep(60)
    
    
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
    print("ELB has been made. URL -> " + str(load_balancer.get('LoadBalancers')[0].get('DNSName')))
    
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
    
    #Destroy everything when user write 'yes'
    destructor(EC2, ELB, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2)
    
    
    
def destructor(ec2_client, elb_client, m4Large_cluster_ids, t2Large_cluster_ids, load_balancer, listener, tg_cluster1, tg_cluster2):
    destroy = False
    while destroy == False:
        answer = input("Enter 'yes' to terminate the instance, elastic load balancer and target groups: ") 
        if answer == "yes":
            
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
            
            destroy = True
        else: 
            continue 
     
main()

