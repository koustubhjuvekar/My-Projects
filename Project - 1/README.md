# 🌍 Enable Cross-Region Backup Replication for EC2 using AWS Backup

**Author: Koustubh Juvekar**
## 🎯 Objective  
The objective of this project is to configure an **AWS Backup Plan** that automatically backs up an EC2 instance in the **primary region (Frankfurt)** and replicates those backups to a **secondary region (Canada)**.  

This ensures:  
✅ Data Durability  
✅ High Availability  
✅ Disaster Recovery  

---

### 📑 Table of Contents
⚙️ Steps<br>
&emsp;&emsp;1. 🌐 Select Regions & Launch EC2<br>
&emsp;&emsp;2. 🖥️ Install & Configure Nginx<br>
&emsp;&emsp;3. 📦 Create Backup Vaults<br>
&emsp;&emsp;4. 📝 Create Backup Plan<br>
&emsp;&emsp;5. 🔗 Assign Resources<br>
&emsp;&emsp;6. ⚡ Run On-Demand Backup<br>
&emsp;&emsp;7. 🔍 Verify Cross-Region Copy<br>
&emsp;&emsp;8. ♻️ Test Restore in Canada<br><br>

✅ Result<br>
🌟 Benefits<br>
⚠️ Issues & Resolutions<br>
🔚 End of Document<br>
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

