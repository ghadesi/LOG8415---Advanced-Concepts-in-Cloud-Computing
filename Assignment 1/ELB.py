def create_load_balancer(client, subnets, sg_id):
    elb = client.create_load_balancer(
        Name='ELB',
        Subnets=subnets,
        SecurityGroups=[sg_id],
        Type='application',
        IpAddressType='ipv4',
        )
    return elb


def create_target_groups(client, vpc_id):
    tg_cluster1 = client.create_target_group(
        Name='cluster1',
        Protocol='HTTP',
        ProtocolVersion='HTTP1',
        Port=80,
        HealthCheckProtocol='HTTP',
        VpcId = vpc_id,
        TargetType='instance'
    )
    
    print("Created target group for cluster 1")

    tg_cluster2 = client.create_target_group(
        Name='cluster2',
        Protocol='HTTP',
        ProtocolVersion='HTTP1',
        Port=80,    
        HealthCheckProtocol='HTTP',
        VpcId = vpc_id,
        TargetType='instance'
    )

    print("Created target group for cluster 2")
    
    return tg_cluster1, tg_cluster2


def create_elb_listener(client, target_group, load_balancer):
    listener = client.create_listener(
        LoadBalancerArn = load_balancer.get('LoadBalancers')[0].get('LoadBalancerArn'),
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'TargetGroupArn': target_group.get('TargetGroups')[0].get('TargetGroupArn'),
                'Type': 'forward',
                'Order': 1,
            },
        ]
    )
    print("Created elb listener")
    return listener


def create_rules(client, listener, tg_cluster1, tg_cluster2):
    print("Creating rules for listener...")
    
    client.create_rule(
        ListenerArn=listener.get('Listeners')[0].get('ListenerArn'),
        Conditions=[
            {
                'Field': 'path-pattern',
                'Values': [
                    '/cluster1',
                ],
            },
        ],
        Priority=1,
        Actions=[
            {
                'TargetGroupArn': tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'),
                'Type': 'forward',
            },
        ],
    )

    client.create_rule(
        ListenerArn=listener.get('Listeners')[0].get('ListenerArn'),
        Conditions=[
            {
                'Field': 'path-pattern',
                'Values': [
                    '/cluster2',
                ],
            },
        ],
        Priority=2,
        Actions=[
            {
                'TargetGroupArn': tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'),
                'Type': 'forward',
            },
        ],
    )
    
    
def register_instances_to_target_groups(client, m4instancesId, t2instancesId, tg_cluster1, tg_cluster2):
    print("registering 5 m4.large instances to target group 1 and 4 t2.large instances to target group 2")
    
    m4Targets = []
    for m4Instance in m4instancesId:
        m4Targets.append({'Id': m4Instance})
    
    client.register_targets(
        TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=m4Targets
    )

    t2Targets = []
    for t2Instance in t2instancesId:
        t2Targets.append({'Id': t2Instance})
        
    client.register_targets(
        TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=t2Targets
    )
    
def deregister_instances_from_target_groups(client, m4instancesId, t2instancesId, tg_cluster1, tg_cluster2):
    print("Deregistering instances from target group")
    
    m4Targets = []
    for m4Instance in m4instancesId:
        m4Targets.append({'Id': m4Instance})
    
    client.deregister_targets(
        TargetGroupArn=tg_cluster1.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=m4Targets
    )

    t2Targets = []
    for t2Instance in t2instancesId:
        t2Targets.append({'Id': t2Instance})
        
    client.deregister_targets(
        TargetGroupArn=tg_cluster2.get('TargetGroups')[0].get('TargetGroupArn'),
        Targets=t2Targets
    )
    