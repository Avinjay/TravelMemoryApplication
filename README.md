# TravelMemoryApplication

# AWS Deployment using Boto3 for Node.js & React

## Overview
This project automates the deployment of a Node.js backend and a React frontend on AWS EC2 instances using Boto3. The setup includes:
- Two EC2 instances via Boto3
- Accessing Application via Public IPs
- Target Group creation
- Target Group linked to both EC2 instances
- Application Load Balancer (ALB)
- ALB listening on ports 80 and 3000
- Domain Configuration in CloudFare
- Setup Auto Scaling Group
- Deployment Verification

## Architecture

![Mern drawio](https://github.com/user-attachments/assets/032e0fcb-f403-4336-aa61-18b9402572de)

## Prerequisites
- AWS Account with necessary permissions
- Python installed (for Boto3 script)
- Boto3 installed (`pip install boto3`)

## Steps

### 1. Setup AWS Resources with Boto3

#### Create EC2 Instances
Create EC2 instances using the `instance_manager.py` script. Modify the script to include:
- Your **AMI ID**
- **Private key name**
- **Security group ID**
- **Subnet ID**
- **Tag key & value**
- Update **home path** and **MongoDB URI** in the user data script

### 2. Access Your Application
Verify Frontend and Backend 
- React Frontend: `http://your-ec2-instance-ip:3000`

  <img width="427" alt="image" src="https://github.com/user-attachments/assets/64523e21-9f79-45b8-923d-b685cd3649d8" />

- Node.js API: `http://your-ec2-instance-ip:3001`

<img width="449" alt="image" src="https://github.com/user-attachments/assets/b5fd461d-d686-46e7-8c81-1a58f41b9e91" />


### 3. Create Target Group
- Go to **Target Groups** > **Create Target Group**
- Select **Instances**
- Configure:
  - Protocol: **HTTP**
  - Port: **3000**
  - VPC: Select your VPC
- Click **Next** and register your **EC2 instances**
- Click **Create Target Group**

### 4. Register EC2 Instances to Target Group
- Select **Instances** and add both EC2 instances
- Choose **port 3000** for forwarding
- Click **Register Targets**

### 5. Create an Application Load Balancer (ALB)
- Go to the [EC2 Console](https://console.aws.amazon.com/ec2/)
- Click **Load Balancers** > **Create Load Balancer**
- Select **Application Load Balancer**
- Configure:
  - Name: **mern-alb**
  - Scheme: **Internet-facing**
  - Listener: **HTTP (80)**, **Custom TCP (3000)**
  - Select the same **VPC** as the EC2 instances
  - Choose **2 public subnets**
- Click **Next** to create the ALB

### 6. Create ALB Listeners & Rules
- Go to **Listeners** in ALB settings
- Add a listener:
  - Port **80** → Forward to Target Group
  - Port **3000** → Forward to Target Group
- Save changes

### 7. Set Up Domain in Cloudflare
- Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
- Select your domain
- Add a **CNAME record**:
  - Name: `hero`
  - Target: `your-alb-dns.amazonaws.com`
- Click **Save**
- Wait for propagation (~5 mins)

#### 8. Setup Auto Scaling Group (ASG)

##### Create Launch Configuration

1. **Create an AMI (Amazon Machine Image) from an Existing EC2 Instance:**
   - Log in to the [EC2 Console](https://console.aws.amazon.com/ec2/).
   - Select your **running EC2 instance**.
   - Click **Actions** > **Image and Templates** > **Create Image**.
   - In the dialog box, provide a name for the AMI (e.g., `mern-backend-frontend-ami`).
   - Click **Create Image**. The AMI creation process will take a few minutes.
   - After the image is created, you can find it under **AMIs** in the EC2 Console.

2. **Create Launch Configuration:**
   - In the **EC2 Console**, go to **Launch Configurations**.
   - Click **Create Launch Configuration**.
   - Choose the **AMI ID** you created earlier.
   - Select your **instance type** (e.g., `t3.micro`).
   - Attach the **security group** that allows HTTP traffic on ports 80 and 3000.
   - Select the **VPC** where your EC2 instances are located.
   - Provide the **key pair** for SSH access.
   - Click **Create Launch Configuration**.

##### Create Auto Scaling Group

1. **Create Auto Scaling Group:**
   - Go to **Auto Scaling Groups** > **Create Auto Scaling Group**.
   - Choose the launch configuration created above.
   - Specify the desired number of instances (e.g., 1) and configure the **minimum** and **maximum** instance counts.
   - Select your **VPC** and **subnets**, use default VPC & subnets, you can refer your existing EC2 details to get these.
   - Enable **Load Balancing** by selecting your **Application Load Balancer (ALB)**.
   - Click **Next** and configure notifications, if needed.
   - Click **Create Auto Scaling Group**.

     <img width="815" alt="image" src="https://github.com/user-attachments/assets/ac55456f-9bc2-4af0-87bf-c56c53be63b8" />
  
  - SNS details whenever instances are created

    <img width="643" alt="image" src="https://github.com/user-attachments/assets/69377bb0-aa34-4bfc-93a0-1b67a6c4b6c8" />


2. **Set Dynamic Scaling Based on CPU Usage:**
   - In the **Auto Scaling Group** settings, configure **CPU utilization alarms** using Amazon **CloudWatch**:
     - **Scale Up**: Set an alarm for when the CPU usage is over **50%** for more than **5 minutes**.

    <img width="515" alt="image" src="https://github.com/user-attachments/assets/abf092ac-f033-4177-bb23-91c0d0ea0e0c" />

       
### 9. Verify the Deployment
- Open `http://hero.yourdomain.com`
- Ensure React frontend loads
- Open browser console & check API calls (`http://your-ec2-ip:3001`)
- Ensure the backend is responding correctly    

## Screenshots

<img width="517" alt="image" src="https://github.com/user-attachments/assets/4464b680-da9c-4f30-bc58-a324759825b6" />

<img width="712" alt="image" src="https://github.com/user-attachments/assets/6039234e-b4cf-4bbe-b120-0e097f7461b7" />

## Contributing
Feel free to open issues or submit pull requests!

## License
MIT
