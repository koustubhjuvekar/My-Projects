## 🌍 `Enable Cross-Region Backup Replication for EC2 using AWS Backup`

**Author:** Koustubh Juvekar <br>
<br>
## 🎯 `Objective`  
The objective of this project is to configure an **_AWS Backup Plan_** that automatically backs up an EC2 instance in the **_Primary region (Frankfurt)_** and replicates those backups to a **_Secondary region (Canada)_**. 

This ensures:  
`1.` Data Durability  
`2.` High Availability  
`3.` Disaster Recovery  
<br>

## 📑 `Table of Contents`
- ⚙️ **Steps**  
  &ensp;&ensp;  `1.` &ensp;Select Regions & Launch EC2  
  &ensp;&ensp;  `2.` &ensp;Install & Configure Nginx  
  &ensp;&ensp;  `3.` &ensp;Create Backup Vaults  
  &ensp;&ensp;  `4.` &ensp;Create Backup Plan  
  &ensp;&ensp;  `5.` &ensp;Assign Resources  
  &ensp;&ensp;  `6.` &ensp;Run On-Demand Backup   
  &ensp;&ensp;  `7.` &ensp;Verify Cross-Region Copy  
  &ensp;&ensp;  `8.` &ensp;Test Restore in Canada  
- &ensp;✅  **Result**
- &ensp;🌟  **Benefits**  
- &ensp;⚠️  **Issues & Resolutions**  
- &ensp;🔚  **End of Document** 
  <br><br>

## ⚙️ `Steps`  
We are creating an automated system where **EC2 backups happen regularly in one region and automatically get replicated to another AWS region.** This way, even if the entire primary region fails (disaster, outage, natural calamity), we can still restore our EC2 instance from the backup stored safely in another region.
### 1. 🌐 **Select Regions and Launch EC2 Instance**
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
  <i><strong>Image 1 :</strong> Launching an EC2 in primary region (Frankfurt - eu-central-1)</i>
</p>

<br>

### 2. 🖥️ **Install and Configure Nginx with Test Application**
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
  <i><strong>Image 2 :</strong> Testing Application output in browser – Primary Region - http://18.192.68.28/test.html</i>
</p><br>


### 3.	🔒 **Create Backup Vaults**
-	In console search, search for AWS Backup. Click on it.
  <img width="1366" height="643" alt="Image 3 Console search for AWS Backup" src="https://github.com/user-attachments/assets/f6b7535a-a04a-4624-9d0d-6085d8cd1adf" />
  <p align="center">
    <i><strong>Image 3 :</strong> Console search for AWS Backup</i>
  </p><br>
<img width="1366" height="643" alt="Image 3 1 - AWS backup console page" src="https://github.com/user-attachments/assets/d79a5177-00d7-440a-b41b-beb0a809f607" />
  <p align="center">
    <i><strong>Image 3.1 :</strong> Console search for AWS Backup</i>
  </p><br>

- Click on Vaults → Click on <kbd>Create New Vault</kbd>

- In the Frankfurt region, create a Backup Vault.
    - **Vault Name** - PrimaryEC2Vault
    - **Vault Type** - Backup Vault
    - **Encryption key** - (default) aws/backup<br>

- **Click on** <kbd>Create Vault</kbd>

<img width="1366" height="640" alt="Image 3 2 - Creating vault" src="https://github.com/user-attachments/assets/a7e7c4aa-36f7-4a37-8996-5130aa04a4c2" />
<p align="center">
    <i><strong>Image 3.2 : </strong> Creating vault</i>
</p><br>

-	After creating vault, click on **Vaults.**
-	List of created vaults displayed here. Click on newly created vault **`PrimaryEC2Vault.`**
-	Details of **`PrimaryEC2Vault`** will be displayed. **Backup Vault created!**

  <img width="1366" height="641" alt="Image 3 3 - Vault created – Vault list – PrimaryEC2Vault" src="https://github.com/user-attachments/assets/162c4ab9-d5fd-43ab-a9cb-ae9a907a43b5" />
  <p align="center">
    <i><strong>Image 3.3 : </strong> Vault created – Vault list – PrimaryEC2Vault</i>
  </p><br>

  <img width="1084" height="552" alt="Image 3 4 - Clicked on PrimaryEC2Vault  -  Details of PrimaryEC2Vault" src="https://github.com/user-attachments/assets/6de70e83-2df1-4c9c-95ab-3cfd622aface" />
  <p align="center">
    <i><strong>Image 3.4 : </strong> Clicked on PrimaryEC2Vault  -  Details of PrimaryEC2Vault</i>
  </p><br>


### 4.	📝 Create Backup Plan
In Frankfurt region (Primary Region), go to **Backup Plans** →  <kbd>Create Backup Plan</kbd> <br>
-	**Start options →** <br>

&emsp;&emsp;▸&emsp;   **Backup plan options -** `Start with a template` <br>
&emsp;&emsp;▸&emsp;   **Templates -** `Daily-35day-Retention` <br>
&emsp;&emsp;▸&emsp;   **Backup plan name –** `MyBackup` <br>

<img width="1365" height="642" alt="Image 4 - Backup plan creating (Start Options)" src="https://github.com/user-attachments/assets/fa01910b-acd5-4826-a04c-1f8ee633c935" />
  <p align="center">
    <i><strong>Image 4 : </strong> Backup plan creating (Start Options)</i>
  </p><br>

- **Backup rules →**  Edit Backup rule or Add backup rule → Backup rule configuration 

&emsp;&emsp;&emsp;&emsp;▸&emsp;  Schedule → 

  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;→&emsp;	**Backup rule name** – `DailyBackups` <br>
  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;→&emsp;	**Backup vault –** Select `PrimaryEC2Vault` <br>
  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;→&emsp;	**Backup frequency –** `Daily` <br>

<img width="1366" height="553" alt="Image 4 1 - Backup plan creating – Edit Backup rule (Backup rule configuration - Schedule)" src="https://github.com/user-attachments/assets/4d57b7c4-f015-484f-bb57-7719b929fff8" />
  <p align="center">
    <i><strong>Image 4.1 : </strong> Backup plan creating – Edit Backup rule (Backup rule configuration - **<strong>Schedule</strong>**)</i>
  </p><br>
