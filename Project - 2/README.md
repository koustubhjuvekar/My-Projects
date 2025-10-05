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
