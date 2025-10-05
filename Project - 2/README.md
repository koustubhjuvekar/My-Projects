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


### ⚙️ `Steps` <br>

We are creating an automated system that continuously monitors EBS volumes, detects gp2 volumes, and converts them to gp3 with built-in logging, alerts, and rollback for safe and efficient operations.
<br>

#### 1. &ensp;🌐 **Launch an EC2 Instance with gp2 Volume** 

- &nbsp;Login to the AWS Management Console. <br>
- &nbsp;Navigate to **EC2 → Instances → Launch Instance**. <br>
- &nbsp;Configure the instance with the following details:
  
  - **Vault Name** - `PrimaryEC2Vault`
  - **Name** - `Project2-EC2Instance`
  - **AMI** - `Amazon Linux 2 (Free Tier Eligible)`
  - **Instance Type** - `t2.micro`
  - **Key Pair** - Select existing or create a new one.
  - **Storage** - Ensure that the root volume is of type `gp2 (default)`.

- Launch the instance and wait until its state = **running**.

- &nbsp;Attach an additional **gp2** EBS volume (e.g., 2 GB).
- &nbsp;Tag the attached volume with:
  - **Key:** `AutoConvert`
  - **Value:** `true`
- &nbsp;Connect to the instance via SSH.


