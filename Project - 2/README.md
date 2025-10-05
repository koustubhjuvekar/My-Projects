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

## ⚙️ `Steps`  <br>
We are creating an automated system that continuously monitors EBS volumes, detects gp2 volumes, and converts them to gp3 with built-in logging, alerts, and rollback for safe and efficient operations.

### 1. 🌐 **Launch an EC2 Instance with gp2 Volume**

<ul>
  <li>&emsp;Login to the AWS Management Console.</li>
  <li>&emsp;Navigate to <b>EC2 → Instances → Launch Instance</b>.</li>
  <li>&emsp;Configure the instance with the following details:</li>
  <ul>
    <li>&emsp;<b>Name:</b> <code>Project2-EC2Instance</code></li>
    <li>&emsp;<b>AMI:</b> <code>Amazon Linux 2 (Free Tier Eligible)</code></li>
    <li>&emsp;<b>Instance Type:</b> <code>t2.micro</code></li>
    <li>&emsp;<b>Key Pair:</b> Select existing or create a new one.</li>
    <li>&emsp;<b>Storage:</b> Ensure that the root volume is of type <code>gp2 (default)</code>.</li>
  </ul>
  <li>&emsp;Launch the instance and wait until its state = <b>running</b>.</li>
  <li>&emsp;Attach an additional <b>gp2</b> EBS volume (e.g., 2 GB).</li>
  <li>&emsp;Tag the attached volume with:</li>
  <ul>
    <li>&emsp;<b>Key:</b> <code>AutoConvert</code></li>
    <li>&emsp;<b>Value:</b> <code>true</code></li>
  </ul>
  <li>&emsp;Connect to the instance via SSH.</li>
</ul>
