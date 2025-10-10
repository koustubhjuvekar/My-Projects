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

- &ensp;⚙️ **Steps**
  
   &ensp;&ensp;  `1.` &ensp;Launch EC2 Instance with gp2 Volume<br>
   &ensp;&ensp;  `2.` &ensp;Add a tag for auto-conversion<br>
   &ensp;&ensp;  `3.` &ensp;Create DynamoDB table<br>
   &ensp;&ensp;  `4.` &ensp;Create SNS topic<br>
   &ensp;&ensp;  `5.` &ensp;Create IAM Role for Lambda and Step Function<br>
   &ensp;&ensp;  `6.` &ensp;Create Lambda functions<br>
   &ensp;&ensp;  `7.` &ensp;Create Step Function<br>
   &ensp;&ensp;  `8.` &ensp;Create EventBridge Rule<br>
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

### 1. &ensp;**Launch an EC2 Instance with gp2 Volume** <br>

#### ▣ &ensp;&nbsp; Go to EC2 Console → Launch Instance <br>

  - &nbsp;Login to the AWS Management Console. Here region is Asia Pacific (Osaka) <br>
  - &nbsp;Navigate to **EC2 → Instances → Launch Instance**. <br>
  - &nbsp;Configure the instance with the following details: <br>
  
    - &ensp;**Name** - `EBS-Demo-Instance`
    - &ensp;**AMI** - `Amazon Linux 2 (Free Tier Eligible)`
    - &ensp;**Instance Type** - `t2.micro`
    - &ensp;**Key Pair** - Select existing or create a new one.
    - &ensp;**Storage** - keep default root volume `(usually gp3)`.
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

    - &ensp;**Volume Type** - `General Purpose SSD (gp2)`
    - &ensp;**Size** - `10 GiB`
    - &ensp;**Name** - `EBS-Demo-Volume` _(You can name volume from tag option.)_ <br>
    

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

### 2. &ensp; **Add a tag for auto-conversion** <br>

- &nbsp;Click on gp2 volume → Scroll down → Click on `Tags` → Click on <kbd>Manage tags</kbd><br>
- &nbsp;Tag the attached volume with: <br>

    - &ensp;**Key** - `AutoConvert`
    - &ensp;**Value** - `"true"`
    
<img width="1366" height="638" alt="Image 2 - Tagging Autoconvert=true" src="https://github.com/user-attachments/assets/0722e536-4be2-4810-974d-fe0e6ab86f8b" />
<p align="center">
  <i><strong>Image 2 :</strong> Tagging Autoconvert= "true" </i>
</p>

<br>

### 3. &ensp; **Create DynamoDB table** <br>

- &nbsp;Go to **DynamoDB Console → Tables → Create Table** <br>

  - &ensp;**Table name** - `EBSConversionLog`
  - &ensp;**Partition key** - `VolumeId (String)`
  - &ensp;**Sort key** - `Timestamp (String)`
  - &ensp;**Billing** - `On-Demand`
    
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

### 4. &ensp; **Create SNS topic** <br>

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
  
  - &ensp;**Type** - `Standard`
  - &ensp;**Name** - `EBSConversionTopic`
  - &ensp;**Display name - _optional_** - `EBSConversionTopic`
    
- &nbsp;Click on → <kbd>Create topic</kbd> <br>

<img width="1366" height="644" alt="Image 4 2 - SNS - Create Topic - options" src="https://github.com/user-attachments/assets/054d0322-80f4-4619-a436-8647bc481128" />
<p align="center">
  <i><strong>Image 4.2 :</strong> SNS - Create Topic - options</i>
</p>
<br>

- &nbsp;Click on **Subscriptions** →  click on <kbd>**Create a subscription**</kbd>

  - &ensp;**Topic ARN** - `arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic` _(It’s the ARN of SNS topic.)_
  - &ensp;**Protocol** - `Email`
  - &ensp;**Endpoint** - `koustubhjuvekar07@gmail.com`

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

### 5. &ensp; **Create IAM Role for Lambda and Step Function** <br> 

#### ▣ &ensp;&nbsp; For Lambda (`LambdaEBSRole`) <br>

- Go to **IAM → Roles → Create Role**
  
   -  &ensp;**Trusted entity type** - `AWS service`
   -  &ensp;**Use case** → Service or use case - `Lambda`
   -  &ensp;**Click on** <kbd>Next</kbd>
     
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
   -  &ensp;`AmazonDynamoDBFullAccess`
   -  &ensp;`AmazonEC2FullAccess`
   -  &ensp;`AmazonSNSFullAccess`
   -  &ensp;`CloudWatchLogsFullAccess`

-  Click on <kbd>Create role</kbd>

-  Name, review and create
   -  &ensp;Role details →
   
      -  &ensp;Role name - `LambdaEBSRole`
      -  &ensp;Description - `Allows Lambda function to call AWS service on your behalf.`
    
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


#### ▣ &ensp;&nbsp;For Step Functions (`StepFunctionsEBSRole`) <br>

-  Go to **IAM → Roles → Create Role**
  
   -  &ensp;**Trusted entity type** - `AWS service`
   -  &ensp;**Use case** → Service or use case - `Step Functions`
   -  &ensp;**Click on** <kbd>Next</kbd>

-  Add Permissions → Permissions policies (1078)
   -  →  Click on `Set permissions boundary - optional`
     -   →  Select `Use a permissions boundary to control the maximum role permissions`
     -   Search and select `CloudWatchLogsFullAccess` `AWSLambdaRole` policies.

-  Name, review and create
   -  &ensp;Role details →
   
      -  &ensp;Role name - `StepFunctionsEBSRole`
      -  &ensp;Description - `Allows Step Functions function to call AWS service on your behalf.`
    
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

### 6. &ensp; **Create Lambda functions** <br>

#### ▣ &ensp;&nbsp; EBSFilterLambda <br>

- Go to **Lambda → Create function**<br>

<img width="1366" height="640" alt="Image 6 - Go to Lambda console" src="https://github.com/user-attachments/assets/20e9bf33-6b51-4801-8aa1-2933151d0e67" />
<p align="center">
  <i><strong>Image 6 :</strong>  Go to Lambda console. </i>
</p>
<br>

- Click on <kbd>Create function</kbd> → Author from scratch
- Basic information
    -  &ensp;Function name - `EBSFilterLambda`
    -  &ensp;Runtime - `Python 3.13`
      
- Permission → Change default execution role →
- Use an existing role →
    -  &ensp;Existing Role - `LambdaEBSRole`

- Click on <kbd>Create function</kbd>

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

- Add environment variable →
  
  -  &ensp;**Key** - `DDB_TABLE`
  -  &ensp;**Value** - `EBSConversionLog`
    
- Click on <kbd>Save</kbd>

  It will be as `DDB_TABLE = EBSConversionLog`


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

- Paste code for filter function [_lambda_function.py_](./1.lambda_function.py)
  
```python
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

- Go to **Lambda → Create function**
- Click on <kbd>Create function</kbd> → Author from scratch
- Basic information
  
    -  &ensp;**Function name** - `EBSModifyLambda`
    -  &ensp;**Runtime** - `Python 3.13`
      
- Permission → Change default execution role →
- Use an existing role →
  
    -  &ensp;**Existing Role** - `LambdaEBSRole`

- Click on <kbd>Create function</kbd>

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

- Add environment variable →
  
  -  &ensp;**Key -** `DDB_TABLE`
  -  &ensp;**Value -** `EBSConversionLog`
  -  &ensp;**Key -**  `SNS_TOPIC_ARN`
  -  &ensp;**Value -** `arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic`
    
- Click on <kbd>Save</kbd>

  It will be as
  -  &ensp;`DDB_TABLE = EBSConversionLog`
  -  &ensp;`SNS_TOPIC_ARN = arn:aws:sns:ap-northeast-3:494341429801:EBSConversionTopic`
  
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

- Paste code for modify function. [_lambda_function.py_](./2.lambda_function.py)

```python
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

-  Go to **Configuration** → General Configuration → Click on <kbd>Edit</kbd> → 
-  Scroll down → Set **Timeout** - `5 min 0 sec`
-  Click on <kbd>Save</kbd>

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


### 7. &ensp;**Create Step Function** <br>

-  Go to **Step Functions → State Machines → Create State Machine**

<img width="1366" height="646" alt="Image 7 - Step Function" src="https://github.com/user-attachments/assets/d85dfee9-bfa7-4fe2-891b-b20b4b04eca1" />
<p align="center">
  <i><strong>Image 7 :</strong> Go to Step Function </i>
</p>
<br>

-  Click on <kbd>Create your own</kbd>

<img width="1366" height="641" alt="Image 7 1 - Step Function - Create your own" src="https://github.com/user-attachments/assets/ee5324ea-0265-45a5-b9fb-f4de6b2dfb33" />
<p align="center">
  <i><strong>Image 7.1 :</strong> Step Function - Create your own </i>
</p>
<br>

-  **Create State Machine**

   -  &ensp;**Step Machine name** - `EBSConversionStateMachine`
   -  &ensp;**Step Machine type** - `Standard`
   -  &ensp;**Click on** <kbd>Continue</kbd>

<img width="1366" height="644" alt="Image 7 1 - Step Function - Creating function" src="https://github.com/user-attachments/assets/5cac791e-faca-4858-ae0c-7a1856c6e67e" />
<p align="center">
  <i><strong>Image 7.1B :</strong> Create state machine </i>
</p>
<br>

-  Click on <kbd>{} Code</kbd>

-  Paste JSON code here. (update ARNs). [_EBSConversionStateMachine_](./3.EBSConversionStateMachine)

```json
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


-  Click on <kbd>{} Config</kbd> → Permission →
  
   -  &ensp;Execution role →
     
      -  &nbsp;Click on Drop down list → Choose and existing role → Select `StepFunctionsEBSRole`

-  Click on <kbd>Create</kbd>

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

### 8. &ensp;**Create EventBridge Rule** <br>

-  Go to **EventBridge → Rules → <kbd>Create Rule</kbd>**
  
<img width="1366" height="642" alt="Image 8 - Eventbridge console" src="https://github.com/user-attachments/assets/3b5d1117-27a9-4b22-b6f0-a28ba2350198" />
<p align="center">
  <i><strong>Image 8 :</strong> Go to Eventbridge console </i>
</p>
<br>

-  Define rule detail → Rule detail →
  
   -  &nbsp;**Name **- `EBSConversionDaily`
   -  &nbsp;**Event bus** - `default`
   -  &nbsp;**Rule type** - `Schedule`

-  Click on <kbd>**Continue to create rule**</kbd>

<img width="1366" height="641" alt="Image 8 1 - Eventbridge console - rule 1" src="https://github.com/user-attachments/assets/92e6b4dd-816e-41f5-8890-c9bd2fe67787" />
<p align="center">
  <i><strong>Image 8.1 :</strong> Eventbridge console - rule 1 </i>
</p>
<br>

<img width="1366" height="590" alt="Image 8 2 - Create rule " src="https://github.com/user-attachments/assets/cb7c1e2d-7a49-464d-b140-72369c735146" />
<p align="center">
  <i><strong>Image 8.2 :</strong> Continue to create rule </i>
</p>
<br>

-  Define schedule → Schedule pattern → <br>`A fine-grained schedule that runs at a specific time, such as 8:00 a.m. PST on the first Monday of every month`
-  Cron Expression
   -  &ensp;`cron(0 2 * * ? *)` (runs daily at 2AM UTC).
   _(Set time as per your requirement. If you want immidiate testing, set time accordingly.)_

-  Next 10 triggers dates and timings will be displayed.
-  Click on <kbd>Next</kbd>

- Select target(s) → Target 1 → Select `AWS service`
  
   -  &nbsp;**Select a target** - `Step Functions state machine`
   -  &nbsp;**State machine** - `EBSConversionStateMachine`
   -  &nbsp;**Execution role** - `Create a new role for this specific resource`
   -  &nbsp;**Role name** - `EventBridgeInvokeStepFunctionRole1`
   -  &nbsp;**Click on** <kbd>Next</kbd>

-  Keep remaining options as it is. At the end, EventBridge Rule will be created.

<img width="1366" height="639" alt="Image 8 3 - Create schedule" src="https://github.com/user-attachments/assets/9cddff6e-b672-426c-ae72-3622d8a2cb57" />
<p align="center">
  <i><strong>Image 8.3 :</strong> Continue to Create schedule </i>
</p>
<br>

<img width="1366" height="637" alt="Image 8 4 - Set Target" src="https://github.com/user-attachments/assets/d3ebab05-1000-4379-be8e-fc3788cf332f" />
<p align="center">
  <i><strong>Image 8.4 :</strong> Continue to Set Target </i>
</p>
<br>

<img width="1366" height="588" alt="Image 8 5 - Set Target IAM role" src="https://github.com/user-attachments/assets/ec191cb7-8402-441d-8f3e-7b3c453d9d3c" />
<p align="center">
  <i><strong>Image 8.5 :</strong> Continue to create IAM role EventBridgeInvokeStepFunctionRole1</i>
</p>
<br>

<img width="1366" height="640" alt="Image 8 6 - Eventbridge rule created" src="https://github.com/user-attachments/assets/cb1ad908-94ff-4268-8836-ba7070ae30e6" />
<p align="center">
  <i><strong>Image 8.6 :</strong> Eventbridge rule created</i>
</p>
<br>

### 9. &ensp;**Testing & Validation** <br>

-  &ensp;Before test -

-  <img width="1366" height="643" alt="Image 9 - Testing before ss" src="https://github.com/user-attachments/assets/d205f993-585e-41ef-8845-462899057676" />
<p align="center">
  <i><strong>Image 9 :</strong> Screenshot before testing</i>
</p>
<br>

-  Manually start **Step Function** execution :

   -  &ensp;Go to Step Functions → State machines → `State machine: EBSConversionStateMachine`
   -  &ensp;Click on <kbd>Start Execution</kbd>

<img width="1366" height="640" alt="Image 9 1 - Step function - Execution start" src="https://github.com/user-attachments/assets/2f5e9603-c296-4538-94cf-c00ad9a87fb5" />
<p align="center">
  <i><strong>Image 9.1 :</strong> Step function - Execution start</i>
</p>
<br>

-  Input: `{}`
-  Click on <kbd>Start execution</kbd>
-  Execution will be started. Wait until success.

<img width="1366" height="644" alt="Image 9 2 - Step function - Execution start -Input" src="https://github.com/user-attachments/assets/3a023d50-4bc1-4d3f-a407-41e5a933b820" />
<p align="center">
  <i><strong>Image 9.2 :</strong> Step function - Execution start - Input</i>
</p>
<br>

<img width="1366" height="641" alt="Image 9 3 - Step function - Execution succeeded" src="https://github.com/user-attachments/assets/233500dc-53b3-42d2-9c62-562eefd0dced" />
<p align="center">
  <i><strong>Image 9.3 :</strong> Step function - Execution start - Execution succeeded</i>
</p>
<br>

-  After succession, graph view of execution will be displayed.

<img width="1366" height="641" alt="Image 9 4 - Flowchart" src="https://github.com/user-attachments/assets/f6b3f24c-acff-4e29-a604-d7df13ea925e" />
<p align="center">
  <i><strong>Image 9.4 :</strong> Graph view</i>
</p>
<br>

-  After run:

   -  &ensp;Go to **DynamoDB → Items tab → Explore Items → Check for DynamoDB audit log** → _should see entry._
     
<img width="1366" height="640" alt="Image 9 5 - DynamoDB audit log" src="https://github.com/user-attachments/assets/0540b11e-a191-4de9-a2c3-436e96765fe8" />
<p align="center">
  <i><strong>Image 9.5 :</strong> DynamoDB audit log</i>
</p>
<br>

<img width="1366" height="642" alt="Image 9 6 - Verify DynamoDB audit log" src="https://github.com/user-attachments/assets/152902dc-363e-4b11-90b5-93a7951fab1b" />
<p align="center">
  <i><strong>Image 9.6  :</strong> Verify DynamoDB audit log</i>
</p>
<br>

-  To check execution step by step and CloudWatch logs showing Lambda output -

   -  &ensp;Go to **CloudWatch → Log groups → /aws/lambda/EBSFilterLambda**

<img width="1366" height="638" alt="Image 9 7A - Converting gpu2 to 3" src="https://github.com/user-attachments/assets/b4c1c82c-583f-4624-a169-851dc239d573" />
<p align="center">
 <i><strong>Image 9.7A  :</strong> CloudWatch → EBSFilterLambda → Converting gp2 to gp3</i>
</p>
<br>

   -  &ensp;Go to **CloudWatch → Log groups → /aws/lambda/EBSModifyLambda**

<img width="1366" height="641" alt="Image 9 7B - Converted gp2 to gp3" src="https://github.com/user-attachments/assets/b0a4cdd5-d922-41cc-8fcc-3a6776ab1f04" />
<p align="center">
 <i><strong>Image 9.7B  :</strong> CloudWatch → EBSModifyLambda → Converted gp2 to gp3</i>
</p>
<br>

-  Step Function execution process → Here, scroll down and check for step column. <br>
-  It will show **ModifyVolumes** Status.

<img width="1366" height="640" alt="Image 9 8 - Converted gp2 to gp3 - step function execution" src="https://github.com/user-attachments/assets/466dc755-a4a1-4a6a-8271-6dfee5b13298" />
<p align="center">
 <i><strong>Image 9.8  :</strong> Converted gp2 to gp3 - step function execution</i>
</p>
<br>

-  Now go to EC2 console → Elastic Block Store → Volumes
-  Check for volume which was gp2 initially, now it is gp3, after conversion.
<br>

<img width="1366" height="644" alt="Image 9 9 - Converted gp2 to gp3 Volume page" src="https://github.com/user-attachments/assets/a610715e-309f-4015-8cba-dc092867b8a4" />
<p align="center">
 <i><strong>Image 9.9  :</strong> Converted gp2 to gp3 Volume </i>
</p>
<br>

-  Created another gp2 volume for testing and attached to EC2 → `vol-005370e741329e7d3`
-  After **Step Function Execution and complete conversion of volume, received email update of service SNS**

<img width="1364" height="640" alt="Image 9 10 - Converted gp2 to gp3 Volume page - created another GPU2" src="https://github.com/user-attachments/assets/7a900c70-2c38-485f-bf9a-ad88080d32fd" />
<p align="center">
 <i><strong>Image 9.10  :</strong> Converted gp2 to gp3 Volume page - created another gp2 - <code>vol-005370e741329e7d3</code> </i>
</p>
<br>

<img width="1366" height="645" alt="Image 9 11 - Converted gp2 to gp3 Volume page - created another GPU2 to check sns - recieve email" src="https://github.com/user-attachments/assets/847609c2-e8c7-4806-b46d-6c5fccaf520f" />
<p align="center">
 <i><strong>Image 9.11  :</strong> Converted gp2 to gp3 Volume page - created another gp2 to check SNS - recieve email for <code>vol-005370e741329e7d3</code> </i>
</p>
<br>

-  DynamoDB logs

<img width="1366" height="642" alt="Image 9 12 - Converted gp2 to gp3 Volume page - Dynamodb" src="https://github.com/user-attachments/assets/0551123d-7c75-4532-9d0d-b71649541509" />
<p align="center">
 <i><strong>Image 9.12  :</strong> Converted gp2 to gp3 Volume page - DynamoDB logs</i>
</p>
<br>

-  Go to Volumes → All volumes are automatically converted to gp3.

<img width="1366" height="639" alt="Image 9 13 - Converted all gp2 to gp3 " src="https://github.com/user-attachments/assets/37aa8481-448a-428e-9f0f-6262894c745b" />
<p align="center">
 <i><strong>Image 9.13  :</strong> Converted all gp2 to gp3 </i>
</p>
<br>

-  Cloudwatch `log groups`

<img width="1366" height="643" alt="Image 9 14 - Cloudwatch for both " src="https://github.com/user-attachments/assets/e60f4ded-cdde-4dc1-8b18-625c4b4b5caa" />
<p align="center">
 <i><strong>Image 9.14  :</strong> Cloudwatch for both groups </i>
</p>
<br>

-  Cloudwatch log Events for `EBSModifyLambda`

<img width="1366" height="642" alt="Image 9 15 - Cloudwatch for modify logd" src="https://github.com/user-attachments/assets/557418da-5796-44b0-8729-5448a007b8bf" />
<p align="center">
 <i><strong>Image 9.15  :</strong> Cloudwatch log Events for EBSModifyLambda </i>
</p>
<br>

-  Cloudwatch log Events for `EBSFilterLambda`

<img width="1366" height="640" alt="Image 9 16 - Cloudwatch for lambdafilter logd" src="https://github.com/user-attachments/assets/ed5b14db-e8cd-4fc8-a453-94da1b803647" />
<p align="center">
 <i><strong>Image 9.15  :</strong> Cloudwatch log Events for EBSFilterLambda </i>
</p>
<br>

