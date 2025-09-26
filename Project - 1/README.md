## 🌍 Enable Cross-Region Backup Replication for EC2 using AWS Backup

Author: Koustubh Juvekar
## 🎯 Objective  
The objective of this project is to configure an **AWS Backup Plan** that automatically backs up an EC2 instance in the **primary region (Frankfurt)** and replicates those backups to a **secondary region (Canada)**.  

This ensures:  
✅ Data Durability  
✅ High Availability  
✅ Disaster Recovery  


## ⚙️ Steps  
- ⚙️ Steps: ](#️-steps) 
  1. ![🌐 Select Regions & Launch EC2](#1-select-regions-and-launch-ec2-instance)  
  2. 🖥️ Install & Configure Nginx(#2-install-and-configure-nginx-with-test-application)  
  3. 📦 Create Backup Vaults(#3-create-backup-vaults)  
  4. 📝 Create Backup Plan(#4-create-backup-plan)  
  5. 🔗 Assign Resources(#5-assign-resources)  
  6. ⚡ Run On-Demand Backup(#6-run-on-demand-backup)  
  7. 🔍 Verify Cross-Region Copy(#7-verify-cross-region-copy)  
  8. ♻️ Test Restore in Canada(#8-test-restore-in-canada)  
- ✅ Result(#-result)  
- 🌟 Benefits(#-benefits-of-cross-region-backup-replication)  
- ⚠️ Issues & Resolutions(#️-issues-encountered-and-resolutions)  
- 🔚 End of Document(#-end-of-document)  

---

## ⚙️ Steps  

### 1. 🌐 Select Regions and Launch EC2 Instance
- **Primary Region:** Europe (Frankfurt – eu-central-1)  
- **Secondary Region:** Canada (Central – ca-central-1)  
- Launched an EC2 instance in Frankfurt (**Amazon Linux t2.micro**).  
- Security Group: Allowed **HTTP (80)** + **SSH (22)**.  

📸 *Insert Screenshot:*  
![Image 1](path/to/image1.png)  

---

### 2. 🖥️ Install and Configure Nginx with Test Application
Install Nginx and set up a test HTML page:  
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
echo "<h1>Hello from Frankfurt</h1>" | sudo tee /usr/share/nginx/html/test.html

