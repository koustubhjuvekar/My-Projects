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

### 3. &ensp;**System preparation** <br>

 - &nbsp;Update packages
   
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
   
 - &nbsp;Install required tools

   ```bash
   sudo apt install -y zip unzip curl jq cron
   ```

 - &nbsp;Verify installations

   ```bash
   zip --version
   jq --version
   curl --version
   ```
   
 - &nbsp;All should show version numbers.
<br>

### 4. &ensp;**Install & configure rclone (google drive)** <br>

 - &nbsp;Install rclone

   ```bash
   curl https://rclone.org/install.sh | sudo bash
   ```
   OR
   
   ```bash
   curl https://rclone.org/install.sh
   ```

 - &nbsp;Configure rclone for Google Drive

   ```bash
   rclone config
   ```
   Follow the prompts carefully:

 - &nbsp;Type `n` → new remote
 - &nbsp;Name → `gdrive`
 - &nbsp;Choose storage → Type `22` (Google Drive – Check list, number may change)
 - &nbsp;Press `Enter` for defaults until it asks:
 - &nbsp;&nbsp;Keep pressing **Enter** until `Option scope` in color.

<img width="1366" height="730" alt="a851bd51-e98b-47e7-8b46-33c0d6955846" src="https://github.com/user-attachments/assets/462d94c1-60a6-424b-981a-29651684755f" />
<p align="center">
  <i><strong>Image 3 :</strong> rclone config </i>
</p>
<br>

- &nbsp;scope> `1` (Full access all files, excluding Application Data Folder.)

<img width="1366" height="729" alt="9bdcf126-d19f-48ac-a3d5-0b4c4c9f3506" src="https://github.com/user-attachments/assets/9f853e06-0d61-4f8f-8dde-596cd0f3fd1e" />
<p align="center">
  <i><strong>Image 4 :</strong> Option Scope </i>
</p>
<br>

- &nbsp;Keep pressing enter until…

  ```bash
  
  Edit advanced config?
  y) Yes
  n) No (default)
  
  y/n> n
  ```
  <br>

  ```bash
  Use web browser to automatically authenticate rclone with remote?
   * Say Y if the machine running rclone has a web browser you can use
   * Say N if running rclone on a (remote) machine without web browser access
  If not sure try Y. If Y failed, try N.
  
  y) Yes (default)
  n) No
  y/n> n
  ```

<img width="1366" height="429" alt="257f18a9-61d6-43b1-94c5-4bc177bbc5a5" src="https://github.com/user-attachments/assets/c7e4ebca-5b8a-4183-9edc-a08dfea9efac" />
<p align="center">
  <i><strong>Image 5 :</strong> rclone authorize "drive" "eyJzY29wZSI6ImRyaXZlIn0" </i>
</p>
<br>

- &nbsp;Now copy rclone command given there

  ```bash
  rclone authorize "drive" "eyJzY29wZSI6ImRyaXZlIn0"
  ```
&nbsp;**wait here and keep as it is…**

---

Now go to your local computer install rclone.

- &nbsp;**Download rclone for Windows**
  
  - Go to: https://rclone.org/downloads/

<img width="898" height="473" alt="214e5842-0afa-4dd5-bb35-8ed1bf045501" src="https://github.com/user-attachments/assets/055cc4fb-ed33-4604-b298-af2deab2d6fe" />
<p align="center">
  <i><strong>Image 6 :</strong> rclone.org/downloads/ </i>
</p>
<br>

- &nbsp;Download as per your OS.
- &nbsp;Under Windows, download the ZIP (64-bit version).
- &nbsp;Extract it, you will see a folder like:

<img width="1366" height="729" alt="f699bf73-0dbe-48e9-b4a4-149baf6fcda2" src="https://github.com/user-attachments/assets/d9c34e6e-ca47-4166-a040-3dc420d5b637" />
<p align="center">
  <i><strong>Image 7 :</strong> rclone folder after extraction </i>
</p>
<br>

- &nbsp;Open Command Prompt in that folder
  
  -	Hold `Shift + Right-click` inside the folder → choose
  -	Open **PowerShell window** here or Open **Command Prompt** here.

<img width="1366" height="728" alt="468a1a42-92c2-4f8f-a8c4-9e6baf7be222" src="https://github.com/user-attachments/assets/6514ae55-6031-4302-a26c-521395014b29" />
<p align="center">
  <i><strong>Image 8 :</strong> Open PowerShell in rclone folder  </i>
</p>
<br>

- &nbsp;**Now you can directly use:**

  -  &nbsp;Now **copy** or **copied rclone command from EC2 console**, paste it here… (add `.\` before copied command)
  <br>

  ```bash
  .\rclone authorize "drive" "eyJzY29wZSI6ImRyaXZlIn0"
  ```

<img width="1366" height="730" alt="42580446-90ea-4d9f-8f19-876921b55c52" src="https://github.com/user-attachments/assets/5ac792bc-414c-429a-ac5d-6a236169bd65" />
<p align="center">
  <i><strong>Image 9 :</strong> PowerShell for rclone sign in  </i>
</p>
<br>

- &nbsp;**Authorize in browser**
   
   - &nbsp;A Google login window will open.
   - &nbsp;Log in → Click `Allow` till end.
   - &nbsp;It will show **Successful** message!

<img width="1366" height="729" alt="b3dbdb4a-9d99-4f54-99f8-cd7b044f2341" src="https://github.com/user-attachments/assets/a969b3f8-f8b8-4660-bf33-4729ea37a666" />
<p align="center">
  <i><strong>Image 10 :</strong> Sign in window for rclone  </i>
</p>
<br>

<img width="1366" height="728" alt="ebf296d9-b7e3-47b2-810a-e7867dae3ccf" src="https://github.com/user-attachments/assets/c7877b8d-f55a-4ffc-995e-6c09f99129dd" />
<p align="center">
  <i><strong>Image 11 :</strong> Sign in Successful  </i>
</p>
<br>

Go back to PowerShell window **where you run rclone command. **

<img width="1366" height="729" alt="2efe92d6-3cac-4959-b4c8-9be825006b8a" src="https://github.com/user-attachments/assets/d432e2d1-cdad-46fd-9532-b96c27bafbe9" />
<p align="center">
  <i><strong>Image 12 :</strong> Result code generated for remote machine  </i>
</p>
<br>

- &nbsp;Copy the result code generated there.
<br>

```bash
  eyJ0b2tlbiI6IntcImFjY2Vzc190b2tlblwiOlwieWEyOS5hMEFRUV9CRFFfVDE1MmJBV09PSEhOYlN5QXNuVUhucm9VOElaczJDNmxWWFpiZ1hkcjc3Q1FULWdvVFlMQnBHX0o2NHpRanlmcHI4VFMycklGcDlLbjdLUXZlUTRZcFcwdmE0T2QzT1MzTC1BREoySnFScUdPNHNiX3E5MXNnaW0yY3lwSFdDcHRESkFUb1NtYlJZVFhlOG9RUUlWTjRLX3VuaVE4Qy1oVWRMSTNqdlphSE5CdUZUN3R5U2E3ZGpGMUNfRXhlSDBhQ2dZS0FXY1NBUkVTRlFIR1gyTWkyb2Q4ZnJYVC1YNW9Pb2VmWWtQSDhnMDIwNlwiLFwidG9rZW5fdHlwZVwiOlwiQmVhcmVyXCIsXCJyZWZyZXNoX3Rva2VuXCI6XCIxLy8wZ0lXbVpGOFJsQm1hQ2dZSUFSQUFHQkFTTndGLUw5SXJNbHFnXzV1ZmJJNU9HbUZoZTZEUnRHVndhd3VMNzZsT0J5eTM2U0dLWUlxUzg2ZnVCeGlnc0RoVHNhYTU3Vk1HZkRBXCIsXCJleHBpcnlcIjpcIjIwMjUtMTAtMjFUMjE6MzQ6MjYuNTE5NjA1NyswNTozMFwiLFwiZXhwaXJlc19pblwiOjM1OTl9In0

```

and now **go back to EC2 console PowerShell!**

---
**Paste copied result code there**

<img width="1366" height="728" alt="c7d8ae85-6a2f-4ed7-a406-a23f09c9f0cb" src="https://github.com/user-attachments/assets/a76d846b-6530-4295-ae9d-f31ed265295f" />
<p align="center">
  <i><strong>Image 13 :</strong> Result code pasted back into EC2 console  </i>
</p>
<br>

```bash
Keep this "gdrive" remote?
y) Yes this is OK (default)
e) Edit this remote
d) Delete this remote

y/e/d> y

```
- &nbsp;Then press q and quit from config option

- &nbsp;**Test it:**

```bash
rclone ls gdrive:
```
- &nbsp;If it **lists files/folders** → working fine.

<img width="1366" height="505" alt="710f15e1-61d5-4f95-9d15-3b9312e114c5" src="https://github.com/user-attachments/assets/06f5f41b-f952-4c46-8736-2e6bc59f177b" />
<p align="center">
  <i><strong>Image 14 :</strong> rclone ls gdrive - list of files/folders in Google drive   </i>
</p>
<br>
  
See, it is syncing all the files from Google drive.



### **5. &ensp;Project directory & config setup**

-  **Create folders**
```bash
mkdir -p ~/MyProject
mkdir -p ~/backups/MyProject
mkdir -p ~/scripts
```

-  **Create a sample project**

```bash
cd ~/MyProject
echo "print('Hello from MyProject')" > app.py
```

-  **Create config file**

_(You will replace your-unique-URL from https://webhook.site)_
Copy** Your unique URL** from there and add it to the given JSON code

<img width="1366" height="728" alt="279449b9-ae57-4cc8-9133-1bdefabb62d0" src="https://github.com/user-attachments/assets/6d9004f8-364a-47bb-8e45-c32db98c8e99" />
<p align="center">
  <i><strong>Image 15 :</strong>Webhook URL </i>
</p>
<br>

```json
cd ~/scripts
cat <<EOF > backup_config.json
{
  "project_name": "MyProject",
  "project_path": "/home/ubuntu/MyProject",
  "backup_base_dir": "/home/ubuntu/backups",
  "remote_name": "gdrive",
  "remote_folder": "ProjectBackups",
  "daily_keep": 7,
  "weekly_keep": 4,
  "monthly_keep": 3,
  "webhook_url": "https://webhook.site/7f18bd10-512b-4858-abae-e875fb082ac6"
}
EOF
```
<br>

Or you can edit or write code using sudo nano ```backup_config.json.```

Save it!

<img width="1366" height="727" alt="c4d60d62-34f6-43fb-a544-8eda1bae71fd" src="https://github.com/user-attachments/assets/b0ffeb2c-ef77-4028-9ed8-4cdf5ae4cb6e" />
<p align="center">
  <i><strong>Image 16 :</strong>  <code> backup_config.json </code></i>
</p>
<br>

You can verify requests coming in webhook.

<img width="1366" height="686" alt="8ece5fa5-40d7-48d0-b91d-0f70a81bcfd6" src="https://github.com/user-attachments/assets/48485bda-ba59-4ee6-b176-760ecebd3114" />
<p align="center">
  <i><strong>Image 17 :</strong>  Webhook Notification</i>
</p>
<br>

### **6.	&ensp;Create the main script**

-  Create the script file

```bash
nano ~/scripts/backup_script.sh
```

Paste Below given code

```bash
#!/bin/bash
# ============================================
# Automated Backup Script with Google Drive Integration
# ============================================

CONFIG_FILE="/home/ubuntu/scripts/backup_config.json"
LOG_FILE="/home/ubuntu/scripts/backup.log"
NOTIFY=true

# ----- Check for --no-notify flag -----
for arg in "$@"; do
  if [ "$arg" == "--no-notify" ]; then
    NOTIFY=false
  fi
done

# ----- Read configuration -----
PROJECT_NAME=$(jq -r '.project_name' $CONFIG_FILE)
PROJECT_PATH=$(jq -r '.project_path' $CONFIG_FILE)
BACKUP_BASE=$(jq -r '.backup_base_dir' $CONFIG_FILE)
REMOTE_NAME=$(jq -r '.remote_name' $CONFIG_FILE)
REMOTE_FOLDER=$(jq -r '.remote_folder' $CONFIG_FILE)
DAILY_KEEP=$(jq -r '.daily_keep' $CONFIG_FILE)
WEEKLY_KEEP=$(jq -r '.weekly_keep' $CONFIG_FILE)
MONTHLY_KEEP=$(jq -r '.monthly_keep' $CONFIG_FILE)
WEBHOOK_URL=$(jq -r '.webhook_url' $CONFIG_FILE)

# ----- Timestamp & Folder structure -----
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DATE_YEAR=$(date +"%Y")
DATE_MONTH=$(date +"%m")
DATE_DAY=$(date +"%d")

BACKUP_DIR="$BACKUP_BASE/$PROJECT_NAME/$DATE_YEAR/$DATE_MONTH/$DATE_DAY"
mkdir -p "$BACKUP_DIR"

BACKUP_FILE="${PROJECT_NAME}_${TIMESTAMP}.zip"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"

# ----- Create backup -----
echo "[$(date)] Starting backup..." | tee -a $LOG_FILE
zip -r "$BACKUP_PATH" "$PROJECT_PATH" >/dev/null
echo "[$(date)] Backup created: $BACKUP_PATH" | tee -a $LOG_FILE

# ----- Upload to Google Drive -----
rclone copy "$BACKUP_PATH" "${REMOTE_NAME}:${REMOTE_FOLDER}" --progress
if [ $? -eq 0 ]; then
    UPLOAD_STATUS="Success"
else
    UPLOAD_STATUS="Failed"
fi

# ----- Rotational Backup Logic -----
echo "[$(date)] Cleaning old backups..." | tee -a $LOG_FILE

find "$BACKUP_BASE/$PROJECT_NAME" -type f -name "*.zip" -mtime +$DAILY_KEEP -delete

if [ "$(date +%u)" -eq 7 ]; then
  find "$BACKUP_BASE/$PROJECT_NAME" -type f -name "*.zip" -mtime +$((7 * WEEKLY_KEEP)) -delete
fi

find "$BACKUP_BASE/$PROJECT_NAME" -type f -name "*.zip" -mtime +$((30 * MONTHLY_KEEP)) -delete

echo "[$(date)] Rotation complete" | tee -a $LOG_FILE

# ----- Notification -----
if [ "$NOTIFY" = true ]; then
  curl -X POST -H "Content-Type: application/json" \
    -d "{\"project\": \"$PROJECT_NAME\", \"date\": \"$(date)\", \"status\": \"$UPLOAD_STATUS\"}" \
    "$WEBHOOK_URL"
  echo "[$(date)] Notification sent ($UPLOAD_STATUS)" | tee -a $LOG_FILE
else
  echo "[$(date)] Notification skipped" | tee -a $LOG_FILE
fi

echo "[$(date)] Backup completed!" | tee -a $LOG_FILE
```

Save it!

<img width="1366" height="728" alt="01b72b6b-1388-459d-b584-fbe77c2161cc" src="https://github.com/user-attachments/assets/d61c1121-0bd9-40e2-9a26-80ba164ba6b7" />
<p align="center">
  <i><strong>Image 18 :</strong>   <code> backup_config.json </code></i>
</p>
<br>

-  **Make it executable**

```bash
chmod +x ~/scripts/backup_script.sh
```

<br>

### **7.	&ensp;Testing manually**

-  **Run the script**
```bash
bash ~/scripts/backup_script.sh
```

You will see the status as backup completed!


So, you can see console like this. Whatever commands we run you can see in the image.

<img width="1366" height="621" alt="6034579b-4307-438b-b1e4-2e64c029fbd1" src="https://github.com/user-attachments/assets/86ae1ee0-473a-4bd4-b3b9-07335016344e" />
<p align="center">
  <i><strong>Image 19 :</strong> Backup status </code></i>
</p>
<br>
