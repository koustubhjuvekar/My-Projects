<img width="1300" height="103" alt="steps1" src="https://github.com/user-attachments/assets/8ecb9133-079b-4136-91e2-1ef774b1656b" />

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
  
  - Launch the instance and wait until its state = **running**.
  
  - &nbsp;Attach an additional **gp2** EBS volume (e.g., 2 GB).
  - &nbsp;Tag the attached volume with:
    - **Key:** `AutoConvert`
    - **Value:** `true`
  - &nbsp;Connect to the instance via SSH.

<img width="1366" height="641" alt="Image 1 - gpu 3 EC2 launching" src="https://github.com/user-attachments/assets/92bbd21b-2f99-4444-baba-387335c66039" />
<p align="center">
  <i><strong>Image 1 :</strong> EC2 launch with gp3 (Default) </i>
</p>
