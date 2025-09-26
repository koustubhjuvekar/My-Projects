## `🌍 Enable Cross-Region Backup Replication for EC2 using AWS Backup`

Author: Koustubh Juvekar
## `🎯 Objective`  
The objective of this project is to configure an **AWS Backup Plan** that automatically backs up an EC2 instance in the **primary region (Frankfurt)** and replicates those backups to a **secondary region (Canada)**.  

This ensures:  
✅ Data Durability  
✅ High Availability  
✅ Disaster Recovery  


## `📑 Table of Contents`
- ⚙️ **Steps**  
  `1.` 🌐 Select Regions & Launch EC2  
  `2.` 🖥️ Install & Configure Nginx  
  `3.` 📦 Create Backup Vaults  
  `4.` 📝 Create Backup Plan  
  `5.` 🔗 Assign Resources  
  `6.` ⚡ Run On-Demand Backup  
  `7.` 🔍 Verify Cross-Region Copy  
  `8.` ♻️ Test Restore in Canada  
- ✅  **Result**
- 🌟  **Benefits**  
- ⚠️  **Issues & Resolutions**  
- 🔚  **End of Document**




## ⚙️ Steps  
We are creating an automated system where **EC2 backups happen regularly in one region and automatically get replicated to another AWS region.** This way, even if the entire primary region fails (disaster, outage, natural calamity), we can still restore our EC2 instance from the backup stored safely in another region.
### 1. 🌐 Select Regions and Launch EC2 Instance
  +  1 primary AWS region (Europe - Frankfurt - eu-central-1)<br>
          -	1 replica AWS region (Canada - Central - ca-central-1)<br>
          -	Launch an EC2 Instance in primary region (here Frankfurt)<br>
          -	Go to the AWS Management Console  EC2  Launch Instance.<br>
          -	Select OS Amazon Linux (or Ubuntu)  Here selected OS is Amazon linux.<br>
          -	Choose an instance type (t2.micro).<br>
          -	Configure security group: Allow HTTP (Port 80) and SSH (Port 22).<br>
          -	Launch the instance and Connect to the instance via SSH.



---

### 2. 🖥️ Install and Configure Nginx with Test Application
Install Nginx and set up a test HTML page:  
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
echo "<h1>Hello from Frankfurt</h1>" | sudo tee /usr/share/nginx/html/test.html

