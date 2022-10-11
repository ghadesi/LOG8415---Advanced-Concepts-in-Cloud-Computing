import time
import boto3
from instances import *


def main():
    
    #initialise the attributs and clients that will be used
    #The follow 3 can change based on who wants to run (the access token is under me: Aleks)
    aws_access_key_id = 'ASIAQJSMAGZDW6NWNBID'
    secret_access_key = 'Nccq12dsGX69KBLGpvHLkt+4Th2VsFPY3fpvj90C'
    session_token = 'FwoGZXIvYXdzEK///////////wEaDAFlYN9PaqL76ueH+yLEATu8xyMZpVHKRfbZPfrSctYEckNgL15pwzu/Ts5ktPCMCNTpt9rRC02EvUiGx8Z2qkf9u5TytPXEreUiMuNasE1ZqYAYiv84DyuZSJMqmf2l0PE2jreqtxqhV7aesBOOlGKy3S801o4D1beXCfCmnc+SQKRQvIt3G3rbVHz7HEtD1P67ukIPlHt5ghJWjLEfuzZf5JBzNNKBrPxzUeDRSR3B7OXuVDqIF4/PjFjuuC8VxKAR2e5+kd1bd25d37UlukmoF/so656SmgYyLQXUDV/R5hyFu9baKBEV3HWqVTRMKjN+53S8ApGlHX3x5bJcYbAnyk6egyMMvg=='
    
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
    
    #Create 5 m4.large instances
    m4Large_cluster_ids = create_m4large_cluster(EC2, keyPairName, securityGroup)
    #Create 4 t2.large instances
    t2Large_cluster_ids = create_t2large_cluster(EC2, keyPairName, securityGroup)
    
    print("Cluster1:")
    print(m4Large_cluster_ids)
    print("Cluster2:")
    print(t2Large_cluster_ids)
    
    # Give some breathing room for instances to initialise 
    print("Sleeping for 120 sec for instances to initialise")
    time.sleep(120)
    
    
    #TODO: we will need to add elb client, then setup load balancer along with target groups and register the instances to their respective target group
    
    #TEMPORARY: delete the instances for now
    terminate_instance_cluster(EC2, m4Large_cluster_ids)
    terminate_instance_cluster(EC2, t2Large_cluster_ids)
    
    
main()