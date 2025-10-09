## 🌍 `Intelligent EBS Volume Optimization Using Lambda, CloudWatch, SNS, DynamoDB & Step Functions`

**Author:** Koustubh Juvekar <br>

**Document:** [![Open or Download PDF](https://img.shields.io/badge/Download-PDF-blue?logo=adobeacrobatreader)](./Project%20-%20Cross-Region%20Backup%20Replication%20for%20EC2%20using%20AWS%20Backup.pdf)

## 🎯 `Objective`  

The objective of this project is to build a serverless automation pipeline that monitors EBS volumes, identifies gp2 volumes, and converts them to gp3 with full logging, alerting, and audit trail.

This ensures: <br>
`1.` Cost Optimization <br>
`2.` Performance Improvement <br>
`3.` Operational Efficiency <br>
`4.` Security & Compliance <br>
`5.` Disaster Recovery (via snapshots/rollback)
<br>

## 📑 `Table of Contents`<br>
- ⚙️ **Steps** <br>
   &ensp;&ensp;  `1.` &ensp;Launch EC2 Instance with gp2 Volume<br>
   &ensp;&ensp;  `2.` &ensp;Create DynamoDB Table<br>
   &ensp;&ensp;  `3.` &ensp;Create SNS Topic & Subscription<br>
   &ensp;&ensp;  `4.` &ensp;Create IAM Role for Lambda<br>
   &ensp;&ensp;  `5.` &ensp;Deploy First Lambda – EBSFilterLambda<br>
   &ensp;&ensp;  `6.` &ensp;Deploy Second Lambda – EBSModifyLambda<br>
   &ensp;&ensp;  `7.` &ensp;Build Step Functions Workflow<br>
   &ensp;&ensp;  `8.` &ensp;Schedule with EventBridge Rule<br>
   &ensp;&ensp;  `9.` &ensp;Testing & Validation<br>
- &ensp;✅ **Result**
- &ensp;🌟 **Benefits**
- &ensp;⚠️ **Issues & Resolutions**
- &ensp;🔐 **Security Best Practices**
- &ensp;🔚 **End of Document** 
<br><br>


## ⚙️ `Steps`

We are creating an automated system that continuously monitors EBS volumes, detects gp2 volumes, and converts them to gp3 with built-in logging, alerts, and rollback for safe and efficient operations.
<br>

### 1. &ensp;🌐 **Launch an EC2 Instance with gp2 Volume** <br>

#### ▣ &ensp;&nbsp; Go to EC2 Console → Launch Instance <br>

  - &nbsp;Login to the AWS Management Console. Here region is Asia Pacific (Osaka) <br>
  - &nbsp;Navigate to **EC2 → Instances → Launch Instance**. <br>
  - &nbsp;Configure the instance with the following details: <br>
  
    - **Name** - `EBS-Demo-Instance`
    - **AMI** - `Amazon Linux 2 (Free Tier Eligible)`
    - **Instance Type** - `t2.micro`
    - **Key Pair** - Select existing or create a new one.
    - **Storage** - keep default root volume `(usually gp3)`.
  - &nbsp;Launch EC2.

<img width="1366" height="641" alt="Image 1 - gpu 3 EC2 launching" src="https://github.com/user-attachments/assets/92bbd21b-2f99-4444-baba-387335c66039" />
<p align="center">
  <i><strong>Image 1 :</strong> EC2 launch with gp3 (Default) </i>
</p>
<br>
<img width="1366" height="643" alt="Image 1 1 - EC2 launched with EBS gp3" src="https://github.com/user-attachments/assets/86e835b5-2a33-476e-995c-918e55a6327b" />
<p align="center">
  <i><strong>Image 1.1 :</strong> EC2 launched with EBS <strong>gp3</strong></i>
</p>

<br>

  #### ▣ &ensp;&nbsp; After launch, create an extra volume: <br>
  - &nbsp;Availability Zone: same as your instance (important!).
  - &nbsp;Go to Elastic Block **Store → Volumes → Create Volume.** <br>

    - **Volume Type** - `General Purpose SSD (gp2)`
    - **Size** - `10 GiB`
    - **Name** - `EBS-Demo-Volume` _(You can name volume from tag option.)_ <br>
    

<img width="1366" height="640" alt="Image 1 2 - Elastic block storage - Volumes - Create new volume" src="https://github.com/user-attachments/assets/fc1daae1-ff3f-4f2f-8f6f-a3f299b53228" />
<p align="center">
  <i><strong>Image 1.2 :</strong> Elastic block storage - Volumes - Create new volume. </i>
</p>
<br>
<img width="1366" height="586" alt="Image 1 3 - Elastic block storage - Volumes - Create new volume" src="https://github.com/user-attachments/assets/d8b90bd5-4443-43e4-8e47-a17e64401e89" />
<p align="center">
  <i><strong>Image 1.3 :</strong> Elastic block storage - Volumes - Create new volume </i>
</p>
<br>
<img width="1366" height="640" alt="Image 1 4 - Volumes created 1 default(gp3) - 1 created (gp2) " src="https://github.com/user-attachments/assets/b35aee5c-b316-4c2a-8656-a2bf88e5d71d" />
<p align="center">
  <i><strong>Image 1.4 :</strong> Volumes created -- 1 default(gp3) - 1 created (gp2) </i>
</p>

<br>

  #### ▣ &ensp;&nbsp; Attach this new volume to your instance. <br>
  - &nbsp;Right-click → Attach Volume → select `EBS-Demo-Instance.`


<img width="1366" height="641" alt="Image 1 5 - Attatch volume to the instance EBS-Demo-Instance" src="https://github.com/user-attachments/assets/24e1bf0c-169d-4339-8664-254f5faf3d05" />
<p align="center">
  <i><strong>Image 1.5 :</strong> Attatch volume to the instance EBS-Demo-Instance </i>
</p>
<br>

- &nbsp;Select instance/EC2 `EBS-Demo-Instance.` from the list.
- &nbsp;Device name `/dev/sdf`
  
- &nbsp;Click on <kbd>**Attach volume**</kbd>

<img width="1366" height="640" alt="Image 1 6 - Attatch volume" src="https://github.com/user-attachments/assets/e197a570-df16-4b37-aef2-2cd57768766d" />
<p align="center">
  <i><strong>Image 1.6 :</strong> Attach volume </i>
</p>
<br>
<img width="1366" height="642" alt="Image 1 7 - Volumes attached" src="https://github.com/user-attachments/assets/100eeaa8-2455-4ade-8124-52cdf87beb21" />
<p align="center">
  <i><strong>Image 1.6 :</strong> Volumes attached to EC2 </i>
</p>

<br>

### 2. &ensp;🌐 **Add a tag for auto-conversion** <br>

- &nbsp;Click on gp2 volume → Scroll down → Click on `Tags` → Click on <kbd>Manage tags</kbd><br>
- &nbsp;Tag the attached volume with: <br>

    - **Key** - `AutoConvert`
    - **Value** - `"true"`
    
<img width="1366" height="638" alt="Image 2 - Tagging Autoconvert=true" src="https://github.com/user-attachments/assets/0722e536-4be2-4810-974d-fe0e6ab86f8b" />
<p align="center">
  <i><strong>Image 2 :</strong> Tagging Autoconvert= "true" </i>
</p>

<br>

### 3. &ensp;🌐 **Create DynamoDB table** <br>

- &nbsp;Go to **DynamoDB Console → Tables → Create Table** <br>

  - **Table name** - `EBSConversionLog`
  - **Partition key** - `VolumeId (String)`
  - **Sort key** - `Timestamp (String)`
  - **Billing** - `On-Demand`
    
- &nbsp;Click on <kbd>**Create table**</kbd>
<br>

<img width="1362" height="643" alt="Image 3 - Go to Dynamodb console" src="https://github.com/user-attachments/assets/d5f673f0-7dab-4349-9bcb-77e74b5d04af" />
<p align="center">
  <i><strong>Image 3 :</strong> Go to Dynamodb console </i>
</p>
<br>
<img width="1366" height="643" alt="Image 3 1 - Dynamodb - Create table" src="https://github.com/user-attachments/assets/3f29f206-caf3-4cbb-b593-0b737d325ada" />
<p align="center">
  <i><strong>Image 3.1 :</strong> Dynamodb - Create table </i>
</p>
<br>
<img width="1366" height="645" alt="Image 3 2 - Createed table -  Table details" src="https://github.com/user-attachments/assets/8dc03bea-dffb-46c0-8593-a284059c71f6" />
<p align="center">
  <i><strong>Image 3.2 :</strong> Created table -  Table details </i>
</p>

<br>

### 4. &ensp;🌐 **Create SNS topic** <br>

- &nbsp;Go to **SNS Console** → Topics → Create Topic**

<img width="1366" height="648" alt="Image 4 - SNS console" src="https://github.com/user-attachments/assets/1b37a0d1-1da1-4d46-a215-874c8ec887d6" />
<p align="center">
  <i><strong>Image 4 :</strong> SNS console</i>
</p>
<br>
<img width="1366" height="643" alt="Image 4 1 - SNS - Create Topic" src="https://github.com/user-attachments/assets/7c580f0b-777a-4944-b88c-d64ae4b1b30b" />
<p align="center">
  <i><strong>Image 4.1 :</strong> SNS - Create Topic</i>
</p>
<br>

- &nbsp;Click on → **Create Topic**
  
  - **Type** - `Standard`
  - **Name** - `EBSConversionTopic`
  - **Display name - _optional_** - `EBSConversionTopic`
    
- &nbsp;Click on → <kbd>Create topic</kbd> <br>

<img width="1366" height="644" alt="Image 4 2 - SNS - Create Topic - options" src="https://github.com/user-attachments/assets/054d0322-80f4-4619-a436-8647bc481128" />
<p align="center">
  <i><strong>Image 4.2 :</strong> SNS - Create Topic - options</i>
</p>
<br>

- &nbsp;Click on **Subscriptions** →  click on <kbd>**Create a subscription**</kbd>

  - **Topic ARN** - `arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic` _(It’s the ARN of SNS topic.)_
  - **Protocol** - `Email`
  - **Endpoint** - `koustubhjuvekar07@gmail.com`

- &nbsp;Click on <kbd>Create subscription</kbd>. <br>
  
<img width="1366" height="643" alt="Image 4 3 - SNS - Email add" src="https://github.com/user-attachments/assets/4e34cf1f-668d-4cc3-b925-38f14c2aef49" />
<p align="center">
  <i><strong>Image 4.3 :</strong> SNS - Add Email</i>
</p>
<br>
  
- &nbsp;Confirm subscription in your mailbox.<br>

<img width="1366" height="647" alt="Image 4 4 - SNS - Email confirm subscription" src="https://github.com/user-attachments/assets/66253093-0697-45cd-bffc-8a0ce9a304ab" />
<p align="center">
  <i><strong>Image 4.4 :</strong> SNS - Email confirm subscription</i>
</p>
<br>

<img width="1366" height="648" alt="Image 4 5 - SNS - Email confirmed" src="https://github.com/user-attachments/assets/50cd12bc-4a63-4666-b8c5-45d24e05d25a" />
<p align="center">
  <i><strong>Image 4.5 :</strong> SNS - Email confirmed</i>
</p>
<br>

### 5. &ensp; **Create IAM Role for Lambda** <br>

#### ▣ &ensp;&nbsp; For Lambda (`LambdaEBSRole`) <br>

-  &nbsp;Go to **IAM → Roles → Create Role**
  
   -  Trusted entity type - `AWS service`
   -  Use case → Service or use case - `Lambda`
   -  click on <kbd>Next</kbd>
     
<img width="1366" height="643" alt="Image 5 - Go to IAM console " src="https://github.com/user-attachments/assets/5c525720-f073-44bc-b41c-08e7aad36ac9" />
<p align="center">
  <i><strong>Image 5 :</strong> Go to IAM console</i>
</p>
<br>

<img width="1366" height="645" alt="Image 5 - IAM roles - create role page 1" src="https://github.com/user-attachments/assets/fbe7be36-4008-4b6e-b9be-bf4c14ce68a6" />
<p align="center">
  <i><strong>Image 5 :</strong> IAM roles - create role page 1 </i>
</p>
<br>

-  Add Permissions → Permissions policies (1078) → Select following permissions(Search in box)
   -  `AmazonDynamoDBFullAccess`
   -  `AmazonEC2FullAccess`
   -  `AmazonSNSFullAccess`
   -  `CloudWatchLogsFullAccess`

-  Click on <kbd>Create role</kbd>

-  Name, review and create
   -  Role details →
   
      -  Role name - `LambdaEBSRole`
      -  Description - `Allows Lambda function to call AWS service on your behalf.`
    
-  Click on <kbd>Create role</kbd>  


<img width="1364" height="641" alt="Image 5 1 - IAM roles - create role page 3 - policies added previously" src="https://github.com/user-attachments/assets/662f7f5d-e6e3-4008-b5a6-2964d6cc3e71" />
<p align="center">
  <i><strong>Image 5.1 :</strong>  IAM roles - create role page 3 - policies added previously</i>
</p>
<br>

<img width="1363" height="640" alt="Image 5 2 - IAM roles - create role page 3" src="https://github.com/user-attachments/assets/ecdcba8c-2092-4802-840a-05ac37608156" />
<p align="center">
  <i><strong>Image 5.2 :</strong>  IAM roles - IAM roles - create role page 3 </i>
</p>
<br>


#### ▣ &ensp;&nbsp; For Step Functions (`StepFunctionsEBSRole`) <br>

- &nbsp;Go to **IAM → Roles → Create Role**
  
  -  Trusted entity type - `AWS service`
  -  Use case → Service or use case - `Step Functions`
  -  click on <kbd>Next</kbd>

-  Add Permissions → Permissions policies (1078)
   -  →  Click on `Set permissions boundary - optional`
     -   →  Select `Use a permissions boundary to control the maximum role permissions`
     -   Search and select `CloudWatchLogsFullAccess` `AWSLambdaRole` policies.

-  Name, review and create
   -  Role details →
   
      -  Role name - `StepFunctionsEBSRole`
      -  Description - `Allows Step Functions function to call AWS service on your behalf.`
    
-  Click on <kbd>Create role</kbd>

<img width="1366" height="639" alt="Image 5 3B - IAM roles - create role for Stepfunction" src="https://github.com/user-attachments/assets/42fd7997-1a4b-4891-9e74-5c873888bb4e" />
<p align="center">
  <i><strong>Image 5.3B :</strong>  IAM roles - create role for Stepfunction </i>
</p>
<br>

<img width="1366" height="601" alt="Image 5 4B - IAM roles - create role for Stepfunction - Attach AWSLambdaRole" src="https://github.com/user-attachments/assets/e119c56b-eb64-48e0-a09c-eaf11580c197" />
<p align="center">
  <i><strong>Image 5.4B :</strong>  IAM roles - Create role for Stepfunction - Attach AWSLambdaRole </i>
</p>
<br>

<img width="1366" height="597" alt="Image 5 5B - IAM roles - create role for Stepfunction - Attach AWSLambdaRole - Use a permissions boundary to control the maximum role permissions" src="https://github.com/user-attachments/assets/8877bbf2-fc4e-492b-87a1-75194b6ec79e" />
<p align="center">
  <i><strong>Image 5.5B :</strong>  IAM roles - create role for Stepfunction - Attach AWSLambdaRole - Use a permissions boundary to control the maximum role permissions </i>
</p>
<br>

<img width="1366" height="642" alt="Image 5 6B - IAM roles - create role for Stepfunction - Page 3" src="https://github.com/user-attachments/assets/85d742ff-a291-4b0f-958e-dff0eaee2f0a" />
<p align="center">
  <i><strong>Image 5.6B :</strong>  IAM roles - create role for Stepfunction - Page 3 </i>
</p>
<br>

<img width="1366" height="639" alt="Image 5 7 - IAM roles created" src="https://github.com/user-attachments/assets/533ea9be-b6bc-472e-ad21-e7e445a37602" />
<p align="center">
  <i><strong>Image 5.7 :</strong>  IAM roles created. </i>
</p>
<br>

### 6. &ensp;🌐 **Create Lambda functions** <br>

#### ▣ &ensp;&nbsp; EBSFilterLambda <br>

- &nbsp;Go to **Lambda → Create function**<br>

<img width="1366" height="640" alt="Image 6 - Go to Lambda console" src="https://github.com/user-attachments/assets/20e9bf33-6b51-4801-8aa1-2933151d0e67" />
<p align="center">
  <i><strong>Image 6 :</strong>  Go to Lambda console. </i>
</p>
<br>

- &nbsp;Click on <kbd>Create function</kbd> → Author from scratch
- &nbsp;Basic information
    -  Function name - `EBSFilterLambda`
    -  Runtime - `Python 3.13`
      
- &nbsp;Permission → Change default execution role →
- &nbsp;Use an existing role →
    -  Existing Role - `LambdaEBSRole`

- &nbsp;Click on <kbd>Create function</kbd>

<img width="1366" height="643" alt="Image 6 1 - Create FUnction - Options" src="https://github.com/user-attachments/assets/3e9d88ad-3d57-416b-81f2-bb51227fc90a" />
<p align="center">
  <i><strong>Image 6.1 :</strong>  Create FUnction - Options. </i>
</p>
<br>

<img width="1366" height="592" alt="Image 6 2 - Create FUnction - Existing role" src="https://github.com/user-attachments/assets/422c3507-fbb0-4da1-a25f-76634c7455eb" />
<p align="center">
  <i><strong>Image 6.2 :</strong>  Create Function - Existing role. </i>
</p>
<br>

- &nbsp;Add environment variable →
  
  -  Key - `DDB_TABLE`
  -  Value - `EBSConversionLog`
    
- &nbsp;Click on <kbd>Save</kbd>

  &nbsp;It will be as `DDB_TABLE = EBSConversionLog`


<img width="1366" height="595" alt="Image 6 3 - Add environment variable" src="https://github.com/user-attachments/assets/efcaeaee-c36c-4add-8f01-e909e7a63efe" />
<p align="center">
  <i><strong>Image 6.3 :</strong>  Add environment variable. </i>
</p>
<br>

<img width="1366" height="643" alt="Image 6 4 - Add environment variable" src="https://github.com/user-attachments/assets/7ab865c1-94bd-4758-bc2b-855af1c9866c" />
<p align="center">
  <i><strong>Image 6.4 :</strong>  Add environment variable. </i>
</p>
<br>

- &nbsp;Paste code for filter function [_lambda_function.py_](./1.lambda_function.py)
  
```
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
```

<img width="1366" height="638" alt="Image 6 5 - Add code" src="https://github.com/user-attachments/assets/733e8329-aed2-4e09-a11f-3f9b48d973d0" />
<p align="center">
  <i><strong>Image 6.5 :</strong>  Add code. </i>
</p>
<br>


#### ▣ &ensp;&nbsp; EBSModifyLambda <br>

- &nbsp;Go to **Lambda → Create function**
- &nbsp;Click on <kbd>Create function</kbd> → Author from scratch
- &nbsp;Basic information
    -  Function name - `EBSModifyLambda`
    -  Runtime - `Python 3.13`
      
- &nbsp;Permission → Change default execution role →
- &nbsp;Use an existing role →
    -  Existing Role - `LambdaEBSRole`

- &nbsp;Click on <kbd>Create function</kbd>

<img width="1366" height="638" alt="Image 6 6B - Create FUnction - EBSModifyLambda" src="https://github.com/user-attachments/assets/f435e2b2-6bf4-4438-9060-66d10d17d125" />
<p align="center">
  <i><strong>Image 6.6B :</strong>  Create FUnction - EBSModifyLambda. </i>
</p>
<br>

<img width="1366" height="591" alt="Image 6 7B - Create FUnction - Existing role" src="https://github.com/user-attachments/assets/90e86736-cc01-48a0-b32d-dfb269dd452d" />
<p align="center">
  <i><strong>Image 6.7B :</strong>  Create Function - Existing role. </i>
</p>
<br>

- &nbsp;Add environment variable →
  
  -  Key - `DDB_TABLE`
  -  Value - `EBSConversionLog`
  -  Key -  `SNS_TOPIC_ARN`
  -  Value - `arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic`
    
- &nbsp;Click on <kbd>Save</kbd>

  &nbsp;It will be as
  -  `DDB_TABLE = EBSConversionLog`
  -  `SNS_TOPIC_ARN = arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic`
  
<img width="1366" height="640" alt="Image 6 8B - Add environment variable" src="https://github.com/user-attachments/assets/f5301e93-cb8c-415b-b7e7-8f53d7b7988c" />
<p align="center">
  <i><strong>Image 6.8B :</strong>  Add environment variable. </i>
</p>
<br>

<img width="1366" height="640" alt="Image 6 9B - Added environment variable" src="https://github.com/user-attachments/assets/e27ea9ef-7aa3-42bd-9db7-c85b93aa0bd3" />
<p align="center">
  <i><strong>Image 6.9B :</strong>  Added environment variable. </i>
</p>
<br>

- &nbsp;Paste code for modify function. [_lambda_function.py_](./2.lambda_function.py)

```
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
```

<img width="1366" height="642" alt="Image 6 10B - Code" src="https://github.com/user-attachments/assets/d3c891c4-6f90-4d0c-a95f-2c5c64f649b7" />
<p align="center">
  <i><strong>Image 6.10B :</strong>  Added code. </i>
</p>
<br>

-  &nbsp;Go to **Configuration** → General Configuration → Click on <kbd>Edit</kbd> → 
-  &nbsp;Scroll down → Set **Timeout** - `5 min 0 sec`
-  &nbsp;Click on <kbd>Save</kbd>

<img width="1366" height="644" alt="Image 6 11B - Edit Timeout = 5min" src="https://github.com/user-attachments/assets/d58825d0-fb4b-4aba-9f2d-c700e74d8900" />
<p align="center">
  <i><strong>Image 6.11B :</strong>  Go to Configuration - Edit Timeout = 5min </i>
</p>
<br>

<img width="1366" height="642" alt="Image 6 12 - Functions created" src="https://github.com/user-attachments/assets/50e09c7d-1fbb-402d-8b6c-3b8fd43151fc" />
<p align="center">
  <i><strong>Image 6.12 :</strong> Lambda Functions created </i>
</p>
<br>


### 7. &ensp;🌐 **Create Step Function** <br>

-  &nbsp;Go to **Step Functions → State Machines → Create State Machine**

<img width="1366" height="646" alt="Image 7 - Step Function" src="https://github.com/user-attachments/assets/d85dfee9-bfa7-4fe2-891b-b20b4b04eca1" />
<p align="center">
  <i><strong>Image 7 :</strong> Go to Step Function </i>
</p>
<br>

-  &nbsp;Click on <kbd>Create your own</kbd>

<img width="1366" height="641" alt="Image 7 1 - Step Function - Create your own" src="https://github.com/user-attachments/assets/ee5324ea-0265-45a5-b9fb-f4de6b2dfb33" />
<p align="center">
  <i><strong>Image 7.1 :</strong> Step Function - Create your own </i>
</p>
<br>

-  &nbsp;**Create State Machine**

   -  Step Machine name - `EBSConversionStateMachine`
   -  Step Machine type - `Standard`
   -  Click on <kbd>Continue</kbd>

<img width="1366" height="644" alt="Image 7 1 - Step Function - Creating function" src="https://github.com/user-attachments/assets/5cac791e-faca-4858-ae0c-7a1856c6e67e" />
<p align="center">
  <i><strong>Image 7.1B :</strong> Create state machine </i>
</p>
<br>

-  &nbsp;Click on <kbd>{} Code</kbd>

-  &nbsp;Paste JSON code here. (update ARNs). [_EBSConversionStateMachine_](./3.EBSConversionStateMachine)

```
{
  "Comment": "State machine to convert gp2 volumes to gp3",
  "StartAt": "FilterVolumes",
  "States": {
    "FilterVolumes": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:ap-northeast-3:494341429801:function:EBSFilterLambda",
      "ResultPath": "$.FilterResult",
      "Next": "CheckVolumesFound"
    },
    "CheckVolumesFound": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.FilterResult.Volumes",
          "IsPresent": true,
          "Next": "ModifyVolumes"
        }
      ],
      "Default": "NoVolumesFound"
    },
    "ModifyVolumes": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:ap-northeast-3:494341429801:function:EBSModifyLambda",
      "InputPath": "$.FilterResult",
      "ResultPath": "$.ModifyResult",
      "End": true
    },
    "NoVolumesFound": {
      "Type": "Pass",
      "Result": "No gp2 volumes found with AutoConvert=true",
      "End": true
    }
  }
}
```

<img width="1365" height="643" alt="Image 7 2 - Step Function - Code" src="https://github.com/user-attachments/assets/bfea0f51-d838-4f35-b89d-b15e8b058cf8" />
<p align="center">
  <i><strong>Image 7.2 :</strong> Step Function - JSON Code </i>
</p>
<br>


-  &nbsp;Click on <kbd>{} Config</kbd> → Permission →
  
   -  Execution role →
     
      -  &nbsp;Click on Drop down list → Choose and existing role → Select `StepFunctionsEBSRole`

-  &nbsp;Click on <kbd>Create</kbd>

<img width="1366" height="643" alt="Image 7 3 - Step Function - Configuration - Execution rule" src="https://github.com/user-attachments/assets/0047eb9e-05f6-42b9-9599-b3e51ba10b87" />
<p align="center">
  <i><strong>Image 7.3 :</strong> Step Function - Configuration - Execution rule <code>StepFunctionsEBSRole</code> </i>
</p>
<br>

<img width="1366" height="642" alt="Image 7 4 - Step Function created" src="https://github.com/user-attachments/assets/bf68d389-3747-4235-a2c9-312da50508b3" />
<p align="center">
  <i><strong>Image 7.4 :</strong> Step Function created </i>
</p>
<br>
