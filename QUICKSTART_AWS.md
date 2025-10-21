# AWS Deployment Quick Start Guide

This guide will get your Face Recognition App running on AWS in 3 different ways.

## Prerequisites

1. AWS Account created
2. AWS CLI installed: `pip install awscli`
3. AWS credentials configured: `aws configure`
4. Docker installed locally
5. Git repository pushed to GitHub

---

## Option 1: ECS Fargate (Recommended - 15 minutes)

### Why ECS Fargate?
- No server management
- Pay only for what you use
- Automatic scaling
- ~$30/month for low traffic

### Quick Deploy Steps

#### Step 1: Get your AWS Account ID

```bash
aws sts get-caller-identity --query Account --output text
```

#### Step 2: Run the infrastructure setup script

```bash
chmod +x setup-ecs-infrastructure.sh
./setup-ecs-infrastructure.sh <your-account-id> us-east-1
```

This creates:
- ECR repositories
- ECS cluster
- CloudWatch log groups
- Task definitions

#### Step 3: Create ECS Services (using the commands from Step 2 output)

Copy and run the backend and frontend service creation commands from the script output.

#### Step 4: Deploy your application

```bash
chmod +x deploy-to-ecs.sh
./deploy-to-ecs.sh <your-account-id> us-east-1
```

#### Step 5: Find your public IP

```bash
aws ecs list-tasks --cluster face-recognition-cluster --service-name frontend-service
aws ecs describe-tasks --cluster face-recognition-cluster --tasks <task-id>
```

Look for the public IP in the output and access: `http://<public-ip>`

#### Step 6: (Optional) Set up Load Balancer

1. Go to EC2 Console → Load Balancers
2. Create Application Load Balancer
3. Add listeners: HTTP (80) and HTTPS (443)
4. Create target groups for backend (5000) and frontend (80)
5. Update ECS services to use the load balancer

---

## Option 2: Elastic Beanstalk (Easiest - 10 minutes)

### Why Elastic Beanstalk?
- Simplest AWS deployment
- Automatic updates and monitoring
- Built-in load balancing
- ~$40/month

### Quick Deploy Steps

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize Elastic Beanstalk

```bash
eb init -p docker face-recognition-app --region us-east-1
```

Select:
- Platform: Docker
- Application name: face-recognition-app
- Default region: us-east-1

#### Step 3: Create environment and deploy

```bash
eb create face-recognition-env
```

This will:
- Create EC2 instances
- Configure load balancer
- Deploy your application
- Set up monitoring

#### Step 4: Open your application

```bash
eb open
```

#### Step 5: Future deployments

```bash
git add .
git commit -m "Update"
eb deploy
```

---

## Option 3: EC2 Instance (Full Control - 20 minutes)

### Why EC2?
- Full server control
- Can install anything
- SSH access
- ~$35/month

### Quick Deploy Steps

#### Step 1: Launch EC2 Instance

```bash
# Create security group
aws ec2 create-security-group \
  --group-name face-recognition-sg \
  --description "Security group for face recognition app"

# Allow HTTP, HTTPS, SSH
aws ec2 authorize-security-group-ingress \
  --group-name face-recognition-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name face-recognition-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name face-recognition-sg \
  --protocol tcp --port 5000 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name face-recognition-sg \
  --protocol tcp --port 8000 --cidr 0.0.0.0/0

# Launch instance (replace with your key pair name)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-groups face-recognition-sg
```

#### Step 2: Connect to instance

```bash
ssh -i your-key.pem ec2-user@<instance-public-ip>
```

#### Step 3: Install Docker

```bash
sudo yum update -y
sudo yum install docker git -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes
exit
```

#### Step 4: Clone and deploy

```bash
ssh -i your-key.pem ec2-user@<instance-public-ip>
git clone https://github.com/<your-username>/face-recognition-app.git
cd face-recognition-app
docker-compose up -d
```

#### Step 5: Access application

Open browser: `http://<instance-public-ip>:8000`

---

## Setting Up GitHub Actions CI/CD

After your initial deployment, set up automatic deployments:

### Step 1: Create AWS IAM User for GitHub Actions

1. Go to IAM Console → Users → Add User
2. Name: `github-actions-deploy`
3. Access type: Programmatic access
4. Attach policies:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonECS_FullAccess`
5. Save Access Key ID and Secret Access Key

### Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add new secrets:
   - `AWS_ACCESS_KEY_ID`: Your access key
   - `AWS_SECRET_ACCESS_KEY`: Your secret key
   - `AWS_ACCOUNT_ID`: Your AWS account ID

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Add AWS deployment configuration"
git push origin main
```

Now every push to `main` branch will automatically deploy to AWS!

---

## Monitoring and Maintenance

### View Logs (ECS)

```bash
aws logs tail /ecs/face-recognition-backend --follow
aws logs tail /ecs/face-recognition-frontend --follow
```

### View Logs (Elastic Beanstalk)

```bash
eb logs
```

### View Logs (EC2)

```bash
ssh -i your-key.pem ec2-user@<instance-ip>
cd face-recognition-app
docker-compose logs -f
```

### Update Application

**ECS:**
```bash
./deploy-to-ecs.sh <account-id> us-east-1
```

**Elastic Beanstalk:**
```bash
eb deploy
```

**EC2:**
```bash
ssh -i your-key.pem ec2-user@<instance-ip>
cd face-recognition-app
git pull
docker-compose down
docker-compose up -d --build
```

---

## Cost Optimization

### Development/Testing
- Use `t3.micro` instances
- Stop instances when not in use
- Use spot instances

### Production
- Use Reserved Instances (save 30-70%)
- Enable auto-scaling
- Use CloudFront CDN
- Monitor with AWS Cost Explorer

---

## Troubleshooting

### Issue: "Access Denied" errors
**Solution:** Check IAM permissions for your user

### Issue: Container fails to start
**Solution:** Check CloudWatch logs for error messages

### Issue: Cannot connect to application
**Solution:** Verify security group rules allow inbound traffic

### Issue: Out of memory
**Solution:** Increase task memory in task definition

---

## Need Help?

- AWS Documentation: https://docs.aws.amazon.com
- File an issue: Your GitHub repo
- AWS Support: AWS Console → Support Center

---

## Next Steps

1. Set up custom domain (Route 53)
2. Add SSL certificate (AWS Certificate Manager)
3. Set up CloudWatch alarms
4. Configure auto-scaling
5. Add database (RDS) if needed
