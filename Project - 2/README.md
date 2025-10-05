## 🌍 `Intelligent EBS Volume Optimization Using Lambda, CloudWatch, SNS, DynamoDB & Step Functions`

**Author:** Koustubh Juvekar <br>

**Document:** [![Open or Download PDF](https://img.shields.io/badge/Download-PDF-blue?logo=adobeacrobatreader)](./Project%20-%20Cross-Region%20Backup%20Replication%20for%20EC2%20using%20AWS%20Backup.pdf)


tep 1: Launch an EC2 Instance with gp2 Volume

Login to the AWS Management Console.

Navigate to EC2 → Instances → Launch Instance.

Configure the instance with the following details:

Name: Project2-EC2Instance

AMI: Amazon Linux 2 (Free Tier Eligible)

Instance Type: t2.micro

Key Pair: Select existing or create a new one.

Storage: Ensure that the root volume is of type gp2 (default).

Launch the instance and wait until its state = running.

Attach an additional gp2 EBS volume (e.g., 2 GB).

Tag the attached volume with:

Key: AutoConvert

Value: true
