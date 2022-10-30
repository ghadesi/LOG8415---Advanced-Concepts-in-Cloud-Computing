from datetime import datetime, timedelta

def analysis(cw_client, c1_ids, c2_ids, tgc1, tgc2):
    """
    Function that does the analysis
    
    :param cw_client: client of Cloudwatch
    :param c1_ids: IDs of m4.large instances
    :param c2_ids: IDs of t2.large instances
    :param tgc1: target group for cluster1
    :param tgc2: target group for cluster2
    """
    results = open("results.txt", "w")

    results.write("ANALYSIS \n")

    #CPU UTILISATION ON ALL CPUS

    results.write('CPU utilisation on all 9 instance:\n')
    results.write('-----------------------------------------------------------\n')
    results.write('CPU utilisation on the instance from cluster1:\n')
    for id in c1_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nCPU Utilization for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('\nCPU utilisation on the instance from cluster2:\n')
    for id in c2_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nCPU Utilization for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('-----------------------------------------------------------\n')

    #NETWORK PACKETS RECEIVED ON ALL CPUS

    results.write('Network Packets Received on all 9 instance:\n')
    results.write('-----------------------------------------------------------\n')
    results.write('Network Packets Received on the instance from cluster1:\n')
    for id in c1_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='NetworkPacketsIn',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nNetwork Packets Received for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('\nNetwork Packets Received on the instance from cluster2:\n')
    for id in c2_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='NetworkPacketsIn',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nNetwork Packets Received for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('-----------------------------------------------------------\n')

    #NETWORK PACKETS SENT ON ALL CPUS

    results.write('Network Packets Sent on all 9 instance:\n')
    results.write('-----------------------------------------------------------\n')
    results.write('Network Packets Sent on the instance from cluster1:\n')
    for id in c1_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='NetworkPacketsOut',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nNetwork Packets Sent for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('\nNetwork Packets Sent on the instance from cluster2:\n')
    for id in c2_ids:
        response = cw_client.get_metric_statistics(
        Period=60,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='NetworkPacketsOut',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        results.write(f"\nNetwork Packets Sent for machine: {id}\n")
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('-----------------------------------------------------------\n')

    #REQUESTS ON CLUSTER 1 AND CLUSTER 2

    results.write('Requests on both cluster:\n')
    results.write('-----------------------------------------------------------\n')
    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='RequestCount',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc1.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nRequests for cluster1: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")


    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='RequestCount',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc2.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nRequests for cluster2: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")

    results.write('-----------------------------------------------------------\n')


    #REQUESTS PER TARGET ON CLUSTER 1 AND CLUSTER 2

    results.write('Requests per target on both cluster:\n')
    results.write('-----------------------------------------------------------\n')
    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='RequestCountPerTarget',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc1.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nRequests per target for cluster1: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")


    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='RequestCountPerTarget',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc2.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nRequests per target for cluster2: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")

    results.write('-----------------------------------------------------------\n')

    #TARGET RESPONSE TIME ON CLUSTER 1 AND CLUSTER 2

    results.write('Target response time on both cluster:\n')
    results.write('-----------------------------------------------------------\n')
    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='TargetResponseTime',
    Namespace='AWS/ApplicationELB',
    Statistics=['Average'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc1.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nTarget response time for cluster1: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")


    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='TargetResponseTime',
    Namespace='AWS/ApplicationELB',
    Statistics=['Average'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc2.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nTarget response time for cluster2: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Average']}\n")

    results.write('-----------------------------------------------------------\n')

    #SUCCESSFUL REQUESTS FOR CLUSTER 1 AND CLUSTER 2

    results.write('Successful requests (2xx) on both clusters:\n')
    results.write('-----------------------------------------------------------\n')
    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='HTTPCode_Target_2XX_Count',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc1.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nSuccessful requests (2xx) for cluster1: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")


    response = cw_client.get_metric_statistics(
    Period=60,
    StartTime=datetime.utcnow() - timedelta(minutes=60),
    EndTime=datetime.utcnow(),
    MetricName='HTTPCode_Target_2XX_Count',
    Namespace='AWS/ApplicationELB',
    Statistics=['Sum'],
    Dimensions=[{'Name':'TargetGroup', 'Value':tgc2.get('TargetGroups')[0].get('TargetGroupArn')}]
    )
    results.write("\nSuccessful requests (2xx) for cluster2: \n")
    if len(response['Datapoints']) == 0:
        results.write("None found\n")
        print(response)
    else:
        for datapoint in response['Datapoints']:
            results.write(f"{datapoint['Timestamp'].astimezone()} --> {datapoint['Sum']}\n")

    results.write('-----------------------------------------------------------\n')
