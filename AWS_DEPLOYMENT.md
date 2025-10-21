# AWS Deployment Guide

This guide covers multiple AWS deployment options for the Face Recognition & Background Removal App.

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Docker installed locally
4. Git repository (GitHub recommended)

## Deployment Options

### Option 1: AWS Elastic Beanstalk (Easiest)
Best for: Quick deployment, managed infrastructure, automatic scaling

### Option 2: AWS ECS with Fargate (Recommended)
Best for: Container-based deployment, no server management, cost-effective

### Option 3: AWS EC2 (Full Control)
Best for: Custom configurations, full server access

---

## Option 1: AWS Elastic Beanstalk Deployment

### Step 1: Install EB CLI

```bash
pip install awsebcli
```

### Step 2: Initialize Elastic Beanstalk

```bash
eb init -p docker face-recognition-app --region us-east-1
```

Select your region when prompted.

### Step 3: Create Environment

```bash
eb create face-recognition-env
```

This will:
- Create an application
- Set up load balancer
- Configure auto-scaling
- Deploy your application

### Step 4: Deploy Updates

```bash
eb deploy
```

### Step 5: Open Application

```bash
eb open
```

### Configuration

See `.ebextensions/` folder for Elastic Beanstalk configurations.

---

## Option 2: AWS ECS with Fargate (Recommended)

### Architecture

- **ECR**: Store Docker images
- **ECS**: Orchestrate containers
- **Fargate**: Serverless compute
- **ALB**: Application Load Balancer
- **CloudWatch**: Logging and monitoring

### Step 1: Create ECR Repositories

```bash
# Create backend repository
aws ecr create-repository --repository-name face-recognition-backend --region us-east-1

# Create frontend repository
aws ecr create-repository --repository-name face-recognition-frontend --region us-east-1
```

### Step 2: Authenticate Docker to ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 3: Build and Push Images

```bash
# Build backend
cd backend
docker build -t face-recognition-backend .
docker tag face-recognition-backend:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/face-recognition-backend:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/face-recognition-backend:latest

# Build frontend
cd ../frontend
docker build -t face-recognition-frontend .
docker tag face-recognition-frontend:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/face-recognition-frontend:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/face-recognition-frontend:latest
```

### Step 4: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name face-recognition-cluster --region us-east-1
```

### Step 5: Register Task Definitions

Use the `aws-ecs/task-definition.json` file:

```bash
aws ecs register-task-definition --cli-input-json file://aws-ecs/task-definition.json
```

### Step 6: Create Services

```bash
# Create backend service
aws ecs create-service \
  --cluster face-recognition-cluster \
  --service-name backend-service \
  --task-definition face-recognition-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"

# Create frontend service
aws ecs create-service \
  --cluster face-recognition-cluster \
  --service-name frontend-service \
  --task-definition face-recognition-frontend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Step 7: Set Up Application Load Balancer

1. Go to AWS Console → EC2 → Load Balancers
2. Create Application Load Balancer
3. Configure target groups for backend (port 5000) and frontend (port 80)
4. Update ECS services to use ALB

---

## Option 3: AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch Instance
   - **AMI**: Amazon Linux 2023 or Ubuntu 22.04
   - **Instance Type**: t3.medium (minimum)
   - **Storage**: 30GB minimum
   - **Security Group**:
     - Port 22 (SSH)
     - Port 80 (HTTP)
     - Port 443 (HTTPS)
     - Port 5000 (Backend API)
     - Port 8000 (Frontend)

### Step 2: Connect to Instance

```bash
ssh -i your-key.pem ec2-user@<instance-public-ip>
```

### Step 3: Install Docker

```bash
# For Amazon Linux 2023
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 4: Clone Repository

```bash
sudo yum install git -y
git clone https://github.com/<your-username>/face-recognition-app.git
cd face-recognition-app
```

### Step 5: Deploy with Docker Compose

```bash
docker-compose up -d
```

### Step 6: Set Up Nginx Reverse Proxy (Optional)

```bash
sudo yum install nginx -y

# Configure nginx to proxy both services
sudo nano /etc/nginx/nginx.conf

# Restart nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Cost Estimates

### Elastic Beanstalk
- **Single instance**: ~$15-30/month
- **Load balanced**: ~$50-100/month
- **High availability**: ~$150-300/month

### ECS Fargate
- **Backend (0.5 vCPU, 1GB RAM)**: ~$15/month
- **Frontend (0.25 vCPU, 0.5GB RAM)**: ~$7/month
- **Total**: ~$25-40/month

### EC2
- **t3.medium**: ~$30/month
- **Storage (30GB)**: ~$3/month
- **Data transfer**: Variable
- **Total**: ~$35-50/month

---

## Environment Variables

### Production Environment Variables

Create a `.env` file for production:

```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<generate-random-secret-key>
ALLOWED_ORIGINS=https://yourdomain.com
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

### AWS Secrets Manager (Recommended)

Store sensitive credentials in AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name face-recognition-app-secrets \
  --secret-string '{"SECRET_KEY":"your-secret-key"}'
```

---

## Domain and SSL Setup

### Step 1: Register Domain (Route 53)

```bash
# Or use existing domain provider
```

### Step 2: Request SSL Certificate (ACM)

1. Go to AWS Certificate Manager
2. Request public certificate
3. Add domain name
4. Validate via DNS or email

### Step 3: Configure Load Balancer

1. Add HTTPS listener (port 443)
2. Attach SSL certificate
3. Redirect HTTP to HTTPS

---

## Monitoring and Logging

### CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/face-recognition

# View logs
aws logs tail /ecs/face-recognition --follow
```

### CloudWatch Alarms

Set up alarms for:
- CPU utilization > 80%
- Memory utilization > 80%
- HTTP 5xx errors
- Request latency

---

## Auto-Scaling Configuration

### ECS Auto-Scaling

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/face-recognition-cluster/backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 5
```

### Scaling Policies

```bash
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/face-recognition-cluster/backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name cpu-scaling-policy \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

---

## Backup and Disaster Recovery

### Known Faces Backup

Use S3 for storing known face images:

```bash
# Create S3 bucket
aws s3 mb s3://face-recognition-known-faces

# Sync known faces
aws s3 sync backend/known_faces/ s3://face-recognition-known-faces/
```

### Database Backup (if using RDS)

Enable automated backups in RDS console.

---

## Security Best Practices

1. **Use VPC**: Deploy resources in private subnets
2. **Security Groups**: Restrict inbound traffic
3. **IAM Roles**: Use least privilege principle
4. **Secrets Manager**: Store sensitive data
5. **WAF**: Add Web Application Firewall
6. **CloudFront**: Use CDN for frontend
7. **Enable logging**: CloudTrail, VPC Flow Logs

---

## CI/CD Pipeline

See `github-actions/` folder for automated deployment pipeline.

---

## Troubleshooting

### Common Issues

**Issue**: Container fails to start
- Check CloudWatch logs
- Verify environment variables
- Check security group rules

**Issue**: Out of memory
- Increase task memory allocation
- Optimize model loading

**Issue**: Slow performance
- Enable CloudFront CDN
- Use Application Load Balancer
- Increase number of tasks

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster face-recognition-cluster --services backend-service

# View task logs
aws ecs describe-tasks --cluster face-recognition-cluster --tasks <task-id>

# SSH into EC2 instance
ssh -i key.pem ec2-user@<instance-ip>

# Docker logs on EC2
docker-compose logs -f
```

---

## Support

For AWS-specific issues, consult:
- AWS Documentation: https://docs.aws.amazon.com
- AWS Support Center
- AWS Forums

For application issues:
- Check GitHub Issues
- Review CloudWatch Logs
