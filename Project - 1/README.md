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
<ul>
  <li>&emsp;1 primary AWS region (Europe - Frankfurt - eu-central-1)</li>
  <li>&emsp;1 replica AWS region (Canada - Central - ca-central-1)</li>
  <li>&emsp;Launch an EC2 Instance in primary region (here Frankfurt)</li>
  <li>&emsp;Go to the AWS Management Console → EC2 → Launch Instance.</li>
  <li>&emsp;Select OS Amazon Linux (or Ubuntu) → Here selected OS is Amazon Linux.</li>
  <li>&emsp;Choose an instance type (t2.micro).</li>
  <li>&emsp;Configure security group: Allow HTTP (Port 80) and SSH (Port 22).</li>
  <li>&emsp;Launch the instance and Connect to the instance via SSH.</li>
</ul>

<img width="1366" height="690" alt="EC2 Primary region launched" src="https://github.com/user-attachments/assets/990a4eb8-ac1a-4135-9148-3685160d2ea1" />
<p align="center">
  <i>Image 1: Launching an EC2 in primary region (Frankfurt - eu-central-1)</i>
</p>


### 2. 🖥️ Install and Configure Nginx with Test Application
Install Nginx and set up a test HTML page:  
```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```
Move into the web directory
```bash
cd /usr/share/nginx/html/
```
Create a simple test page
```bash
sudo nano test.html
```
Insert this code: (or you can add your html page for test)
```bash
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cross-Region Backup Test</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(to right, #00b09b, #96c93d);
      color: white;
      text-align: center;
      padding-top: 15%;
    }
    h1 {
      font-size: 3em;
      margin-bottom: 20px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    p {
      font-size: 1.2em;
      background: rgba(0, 0, 0, 0.4);
      display: inline-block;
      padding: 10px 20px;
      border-radius: 10px;
    }
  </style>
</head>
<body>
  <h1> Cross-Region Backup Replication Demo</h1>
  <p>This is Testing Application.<br><br>This EC2 instance is running on <strong>Nginx</strong>.<br><br>
     This is EC2 in Primary region <strong>Europe - Frankfurt - eu-central-1.</strong><br>
     A replica is created in the Canada region.<strong>Canada - Central - ca-central-1.</strong></p>
</body>
</html>
```
Save it **(Ctrl + X)** --> **(press y)** --> Press **Enter**.
```bash
sudo systemctl reload nginx
```

This is testing HTML page. Run in Primary region http://18.192.68.28/test.html

<img width="1366" height="686" alt="ss1" src="https://github.com/user-attachments/assets/20f7b2ed-b1f4-40ee-9c9a-1cd400df974a" />
<p align="center">
  <i>Image 2: Testing Application output in browser – Primary Region - http://18.192.68.28/test.html</i>
</p><br>


### 3.	🔒 Create Backup Vaults
-	In console search, search for AWS Backup. Click on it.
  <img width="1366" height="643" alt="Image 3 Console search for AWS Backup" src="https://github.com/user-attachments/assets/f6b7535a-a04a-4624-9d0d-6085d8cd1adf" />
  <p align="center">
    <i>Image 3: Console search for AWS Backup</i>
  </p><br>
<img width="1366" height="643" alt="Image 3 1 - AWS backup console page" src="https://github.com/user-attachments/assets/d79a5177-00d7-440a-b41b-beb0a809f607" />
  <p align="center">
    <i>Image 3.1: AWS backup console page</i>
  </p><br>

Click on Vaults ▶ <br><img width="150" height="72" alt="Create_Vault-removebg-preview" margin="25px" src="https://github.com/user-attachments/assets/5f931609-2a94-465d-82fd-dcfcbc90bbdd" /><br>

In the Frankfurt region, create a Backup Vault.
•	Vault Name - PrimaryEC2Vault
•	Vault Type - Backup Vault
•	Encryption key - (default) aws/backup
Click on    Create vault


