# Enable Cross-Region Backup Replication for EC2 using AWS Backup
**Author: Koustubh Juvekar**

## Objective
The goal of this project was to configure an **AWS Backup Plan** to automatically back up an **EC2 instance** in a primary AWS region and replicate the recovery points (AMIs) to a secondary AWS region. [cite_start]This setup ensures **data durability** and **disaster recovery (DR)** readiness across geographical locations[cite: 716, 717].

We created an automated system where EC2 backups happen regularly in one region and are automatically replicated to another AWS region. [cite_start]This way, even if the entire primary region fails (disaster, outage, natural calamity), we can still restore our EC2 instance from the backup stored safely in the secondary region[cite: 718, 719].

## Regions Used
* [cite_start]**Primary AWS Region:** Europe - Frankfurt (`eu-central-1`)[cite: 720, 728].
* [cite_start]**Replica AWS Region:** Canada - Central (`ca-central-1`)[cite: 720, 729].

## Steps Implemented

### 1. EC2 Instance Setup (Primary Region: Frankfurt)
1.  Launch an EC2 Instance:** Launched a **t2.micro** instance using **Amazon Linux** in the Frankfurt region
2.  Security Group:** Configured the security group to allow **HTTP (Port 80)** and **SSH (Port 22)
3.  Install & Configure Nginx:** Connected to the instance via SSH and installed Nginx along with a test application page (`test.html`)

**Shell Commands for Nginx Setup:**
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
# Check status: sudo systemctl status nginx

cd /usr/share/nginx/html/
sudo nano test.html
