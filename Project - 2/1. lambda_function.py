import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    print("Starting EBS Filter Lambda")
    ec2 = boto3.client('ec2')
    dynamodb = boto3.client('dynamodb')
    
    try:
        # Get all gp2 volumes with AutoConvert=true tag
        response = ec2.describe_volumes(
            Filters=[
                {'Name': 'volume-type', 'Values': ['gp2']},
                {'Name': 'tag:AutoConvert', 'Values': ['"true"']}
            ]
        )
        
        volumes = response['Volumes']
        print(f"Found {len(volumes)} gp2 volumes with AutoConvert=true")
        
        volume_ids = []
        
        # Process each volume
        for volume in volumes:
            volume_id = volume['VolumeId']
            print(f"Processing volume: {volume_id}")
            volume_ids.append(volume_id)
            
            # Record in DynamoDB
            dynamodb.put_item(
                TableName=os.environ['DDB_TABLE'],
                Item={
                    'VolumeId': {'S': volume_id},
                    'Timestamp': {'S': datetime.utcnow().isoformat()},
                    'Status': {'S': 'PENDING'},
                    'Action': {'S': 'Identified'}
                }
            )
            print(f"Recorded {volume_id} in DynamoDB")
        
        # Return in simplified format for Step Functions
        return {
            'statusCode': 200,
            'Volumes': volume_ids
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'Volumes': []
        }
