# Enable Cross-Region Backup Replication for EC2 using AWS Backup

## 📌 Objective
The objective of this project is to configure an AWS Backup Plan that automatically backs up an EC2 instance in the primary region and replicates those backups to a secondary AWS region.  
This ensures **data durability, high availability, and disaster recovery readiness** across geographically separated regions.

---

## ⚙️ Steps

### 1. Select Regions and Launch EC2 Instance
- **Primary Region:** Europe (Frankfurt – eu-central-1)  
- **Secondary Region:** Canada (Central – ca-central-1)  
- Launched an EC2 instance in Frankfurt using Amazon Linux (t2.micro).  
- Configured Security Group to allow **HTTP (Port 80)** and **SSH (Port 22)**.  
- Connected to the instance via SSH.  

![Image 1](path/to/image1.png)  

---

### 2. Install and Configure Nginx with Test Application
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
Created a simple HTML test page in /usr/share/nginx/html/test.html.


3. Create Backup Vaults
Created PrimaryEC2Vault in Frankfurt.

Created SecondaryEC2VaultCanada in Canada.





4. Create Backup Plan
Used AWS Backup template Daily-35day-Retention.

Configured rule:

Backup Vault: PrimaryEC2Vault

Frequency: Daily

Lifecycle: Warm → Cold storage

Added Copy Rule: Copy to Canada (ca-central-1) → SecondaryEC2VaultCanada








5. Assign Resources
Assigned EC2 instance (i-0545b6e883c95a7c5) to backup plan.

IAM Role used: AWSBackupDefaultServiceRole




6. Run On-Demand Backup
Triggered manual backup from Frankfurt.

Backup stored in PrimaryEC2Vault.






7. Verify Cross-Region Copy
Verified Copy Jobs in Frankfurt.

Status: Completed → Confirmed replication to Canada.



8. Test Restore in Canada
Opened SecondaryEC2VaultCanada.

Verified recovery points created.

Launched EC2 from replicated AMI in Canada.

Verified same test application output.







✅ Result
Cross-Region Backup Replication for EC2 using AWS Backup was successfully implemented.
Backups from Frankfurt were automatically copied to Canada, and the instance was restored from the replicated backup in Canada.

🌟 Benefits of Cross-Region Backup Replication
Disaster Recovery (DR): Protects workloads if primary region fails.

Data Durability: Ensures backups are safe across regions.

Compliance & Governance: Supports regulatory requirements.

High Availability: Enables faster recovery in secondary region.

⚠️ Issues Encountered and Resolutions
Cross-Region Copy Delay

Recovery points did not appear immediately because only new backups are copied.

Resolved by creating on-demand backups in Frankfurt.

Restore Failure via AWS Backup Console

Restore failed due to missing VPC/subnet/security groups in Canada.

Resolved by launching EC2 directly from AMI in Canada and selecting correct networking.
