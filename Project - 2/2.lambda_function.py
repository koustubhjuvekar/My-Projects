import boto3
import json
import os
from datetime import datetime

def lambda_handler(event, context):
    print(f"EBSModifyLambda started with event: {event}")
    
    ec2 = boto3.client('ec2')
    dynamodb = boto3.client('dynamodb')
    sns = boto3.client('sns')
    
    try:
        # Get volumes from Step Functions input
        volumes = event.get('Volumes', [])
        print(f"Processing {len(volumes)} volumes: {volumes}")
        
        if not volumes:
            return {
                'statusCode': 400,
                'body': json.dumps('No volumes provided in event')
            }
        
        converted_volumes = []
        
        for volume_id in volumes:
            print(f"Processing volume: {volume_id}")
            
            # Describe volume
            response = ec2.describe_volumes(VolumeIds=[volume_id])
            volume = response['Volumes'][0]
            
            # Check volume type
            current_type = volume['VolumeType']
            tags = {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
            
            print(f"Volume {volume_id}: type={current_type}, AutoConvert={tags.get('AutoConvert')}")
            
            if current_type == 'gp2' and tags.get('AutoConvert') == '"true"':
                print(f"Converting volume {volume_id} from gp2 to gp3")
                
                # Convert to gp3
                ec2.modify_volume(VolumeId=volume_id, VolumeType='gp3')
                
                # Update DynamoDB
                dynamodb.put_item(
                    TableName=os.environ['DDB_TABLE'],
                    Item={
                        'VolumeId': {'S': volume_id},
                        'Timestamp': {'S': datetime.utcnow().isoformat()},
                        'Status': {'S': 'COMPLETED'},
                        'Action': {'S': 'Converted to gp3'}
                    }
                )
                
                # Send SNS notification
                try:
                    sns_response = sns.publish(
                        TopicArn=os.environ['SNS_TOPIC_ARN'],
                        Subject='✅ EBS Volume Converted Successfully',
                        Message=f'''EBS Volume Conversion Complete!

Volume ID: {volume_id}
Conversion: gp2 → gp3
Timestamp: {datetime.utcnow().isoformat()} UTC
Status: SUCCESS

Your EBS volume has been successfully converted from gp2 to gp3.
This may result in cost savings and improved performance.

AWS EBS Conversion Service'''
                    )
                    print(f"SNS notification sent: {sns_response['MessageId']}")
                except Exception as sns_error:
                    print(f"SNS notification failed: {str(sns_error)}")
                
                converted_volumes.append(volume_id)
                print(f"Successfully converted {volume_id} to gp3")
            else:
                print(f"Skipping {volume_id}: type={current_type}, AutoConvert={tags.get('AutoConvert')}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Converted {len(converted_volumes)} volumes: {converted_volumes}")
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
        # Send error notification
        try:
            sns.publish(
                TopicArn=os.environ['SNS_TOPIC_ARN'],
                Subject='❌ EBS Volume Conversion Failed',
                Message=f'''EBS Volume Conversion Error!

Error: {str(e)}
Timestamp: {datetime.utcnow().isoformat()} UTC
Event: {json.dumps(event)}

Please check CloudWatch logs for more details.

AWS EBS Conversion Service'''
            )
        except:
            pass
        
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
