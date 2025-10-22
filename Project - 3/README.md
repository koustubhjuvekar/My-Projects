# 🌍 `Automated Backup and Rotation Script with Google Drive Integration`

## `Scenario:`

-	You are responsible for creating a backup management script for a project hosted on GitHub. 
-	The project consists of important code files that need to be regularly backed up.
-	The script should also implement a rotational backup strategy and integrate with Google Drive to push the backups to a specified folder. 
-	On successful backup, a notification cURL request should be triggered.

## 🎯 `Objective:`
Build a fully automated shell or Python script that: 
-	Backs up a specified project directory 
-	Organizes and stores backups in a timestamped format 
-	Integrates with Google Drive using CLI tools 
-	Implements a rotational backup strategy (daily, weekly, monthly) 
-	Sends a cURL request on successful backup 
-	Logs the process and supports configuration

This ensures: <br>

  `1.` Data Protection and Versioning <br>
  `2.` Seamless Cloud Synchronization <br>
  `3.` Storage Efficiency via Rotation <br>
  `4.` Automation & Reliability <br>
  `5.` Auditability through Logs and Notifications <br>
<br>

## 📑 `Table of Contents` <br>

- &ensp;⚙️ **Steps**
  
    &ensp;&ensp;  `1.` &ensp;Install Required Tools (rclone / gdrive) <br>
    &ensp;&ensp;  `2.` &ensp;Configure Google Drive Integration <br>
    &ensp;&ensp;  `3.` &ensp;Create Project Directory and Backup Structure <br>
    &ensp;&ensp;  `4.` &ensp;Write Backup Script (Shell / Python) <br>
    &ensp;&ensp;  `5.` &ensp;Implement Rotational Backup Logic (Daily, Weekly, Monthly) <br>
    &ensp;&ensp;  `6.` &ensp;Add Logging and Notification via cURL <br>
    &ensp;&ensp;  `7.` &ensp;Test Backup, Rotation, and Upload <br>
    &ensp;&ensp;  `8.` &ensp;Configure Crontab for Automation <br>
    &ensp;&ensp;  `9.` &ensp;Validate Logs and Restore from Backup <br> 
- &ensp;✅ Result
- &ensp;🌟 Benefits
- &ensp;⚠️ Issues & Resolutions
- &ensp;🔐 Security Best Practices 
- &ensp;🔚 End of Document
<br><br>


## ⚙️ `Steps`

This project automates the process of creating, storing, and managing backups for a GitHub-hosted project.
It compresses the project into a timestamped ZIP file, uploads it to Google Drive via rclone, maintains a rotation policy (daily, weekly, monthly), and sends a notification upon success.
Follow the below steps to set up, configure, and test the entire automation from an AWS EC2 instance.

### 1. &ensp;**Launch ec2 instance** <br>

  - &nbsp;Open AWS Management Console
  - &nbsp;Navigate to EC2 → Instances → Launch Instance
    
      - &nbsp;**Name** – `BackupAutomationServer`
      - &nbsp;**AMI** - `Ubuntu Server 22.04 LTS`
      - &nbsp;**Instance type** - `t2.micro (Free tier)`
      - &nbsp;**Key pair** - `Create new or use existing (download .pem file)`
      - &nbsp;**Network settings** - `Allow SSH (port 22)`
        
- &nbsp;Launch instance!

<img width="1366" height="642" alt="Ec2" src="https://github.com/user-attachments/assets/31ca166f-e52a-4419-91f2-285160064374" />
<p align="center">
  <i><strong>Image 1 :</strong> EC2 launched (Default) </i>
</p>
<br>

### 2. &ensp;**Connect to EC2** <br>

 - &nbsp;Open PowerShell or any SSHclient. Connect to EC2.

   ```bash
   &nbsp;ssh -i "C:\Users\koust\Downloads\BackupAutomation.pem" ubuntu@13.215.185.143
   ```
   
<img width="1366" height="725" alt="79f08726-a589-41de-8853-c523843dd2c6" src="https://github.com/user-attachments/assets/6e22425d-f933-49c3-b39e-dba7f7682f48" />
<p align="center">
  <i><strong>Image 2 :</strong> Connected to EC2 using SSH </i>
</p>
<br>

