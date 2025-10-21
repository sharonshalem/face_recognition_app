#!/bin/bash

# AWS ECS Infrastructure Setup Script
# This script creates all necessary AWS resources for ECS deployment
# Usage: ./setup-ecs-infrastructure.sh <aws-account-id> <aws-region>

set -e

AWS_ACCOUNT_ID=$1
AWS_REGION=${2:-us-east-1}
CLUSTER_NAME="face-recognition-cluster"

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Error: AWS Account ID is required"
    echo "Usage: ./setup-ecs-infrastructure.sh <aws-account-id> [aws-region]"
    exit 1
fi

echo "========================================="
echo "Setting up AWS ECS Infrastructure"
echo "========================================="
echo ""

# Step 1: Create ECR Repositories
echo "[1/7] Creating ECR repositories..."
aws ecr create-repository --repository-name face-recognition-backend --region $AWS_REGION 2>/dev/null || echo "Backend repository already exists"
aws ecr create-repository --repository-name face-recognition-frontend --region $AWS_REGION 2>/dev/null || echo "Frontend repository already exists"

# Step 2: Create ECS Cluster
echo "[2/7] Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION 2>/dev/null || echo "Cluster already exists"

# Step 3: Create CloudWatch Log Groups
echo "[3/7] Creating CloudWatch log groups..."
aws logs create-log-group --log-group-name /ecs/face-recognition-backend --region $AWS_REGION 2>/dev/null || echo "Backend log group already exists"
aws logs create-log-group --log-group-name /ecs/face-recognition-frontend --region $AWS_REGION 2>/dev/null || echo "Frontend log group already exists"

# Step 4: Create IAM Execution Role (if not exists)
echo "[4/7] Checking IAM execution role..."
aws iam get-role --role-name ecsTaskExecutionRole --region $AWS_REGION 2>/dev/null || \
echo "Please create ecsTaskExecutionRole in IAM console with AmazonECSTaskExecutionRolePolicy"

# Step 5: Register Task Definitions
echo "[5/7] Registering task definitions..."
echo "Updating task definition files with your account ID..."
sed -i "s/<your-account-id>/$AWS_ACCOUNT_ID/g" aws-ecs/task-definition-backend.json
sed -i "s/<your-account-id>/$AWS_ACCOUNT_ID/g" aws-ecs/task-definition-frontend.json

aws ecs register-task-definition --cli-input-json file://aws-ecs/task-definition-backend.json --region $AWS_REGION
aws ecs register-task-definition --cli-input-json file://aws-ecs/task-definition-frontend.json --region $AWS_REGION

# Step 6: Get VPC and Subnet information
echo "[6/7] Getting VPC information..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text --region $AWS_REGION)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text --region $AWS_REGION | tr '\t' ',')
SECURITY_GROUP=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" "Name=group-name,Values=default" --query "SecurityGroups[0].GroupId" --output text --region $AWS_REGION)

echo "VPC ID: $VPC_ID"
echo "Subnet IDs: $SUBNET_IDS"
echo "Security Group: $SECURITY_GROUP"

# Step 7: Instructions for creating services
echo ""
echo "[7/7] Infrastructure setup complete!"
echo ""
echo "========================================="
echo "Next Steps:"
echo "========================================="
echo ""
echo "1. Create ECS Services manually in AWS Console OR use these commands:"
echo ""
echo "Backend Service:"
echo "aws ecs create-service \\"
echo "  --cluster $CLUSTER_NAME \\"
echo "  --service-name backend-service \\"
echo "  --task-definition face-recognition-backend \\"
echo "  --desired-count 1 \\"
echo "  --launch-type FARGATE \\"
echo "  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}\" \\"
echo "  --region $AWS_REGION"
echo ""
echo "Frontend Service:"
echo "aws ecs create-service \\"
echo "  --cluster $CLUSTER_NAME \\"
echo "  --service-name frontend-service \\"
echo "  --task-definition face-recognition-frontend \\"
echo "  --desired-count 1 \\"
echo "  --launch-type FARGATE \\"
echo "  --network-configuration \"awsvpcConfiguration={subnets=[$SUBNET_IDS],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}\" \\"
echo "  --region $AWS_REGION"
echo ""
echo "2. Set up Application Load Balancer in AWS Console"
echo "3. Configure security groups to allow traffic"
echo "4. Run ./deploy-to-ecs.sh $AWS_ACCOUNT_ID $AWS_REGION to deploy"
echo ""
