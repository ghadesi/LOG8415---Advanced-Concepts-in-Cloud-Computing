import boto3
from datetime import datetime, timedelta

def main():

    aws_access_key_id = 'ASIAQJSMAGZDT52JX4MM'
    secret_access_key = 'dVq3C7vYNcHs6gwsWfUREkU+YMAB8Mms1cQXUvJs'
    session_token = 'FwoGZXIvYXdzED8aDLONnpYzhG7cywXQjSLEAS5IPHCLXfBUPX3BhWOw0bQ/BoBaSYDK4voOBvNG1bU9AF7Ra5niTOxP2WeZ1gMDWU3zFAfJM3IKUTXdARNI8OQYaFwyhXV+t3lmw0ZJKoA+KDqAi+rewK27CAI2ZyEAkNQSIk1pSZ7av5nGgo8VH7P9UL6Zlb5OpvlLLylYqxLLXzIJH/iFNJHq5beJht4k6EaureKn5LnZZbpP+8ZRVFL/yM8246JtGCLxceHgGrwTGB0roqHYOpSClZ6+D2dl8LmuOdwo3OmxmgYyLfZxCu66DT7R8bOOakkAA0eRPH97gJW79xE6rlJuFqr6GfzFeeWkneN23reerg=='
    client = boto3.client('cloudwatch',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
    region_name= 'us-east-1'
    )


    for id in ['i-0432eec2a235d3b4b']:
        cpu_utilization = client.get_metric_statistics(
        Period=300,
        StartTime=datetime.utcnow() - timedelta(minutes=60),
        EndTime=datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name':'InstanceId', 'Value':id}]
        )
        print(f"CPU Utilization for machine: {id}")
        print(f"Average: {cpu_utilization}\n")

main()