#!/bin/bash

# AWS ECS Deployment Script for Face Recognition App
# Usage: ./deploy-to-ecs.sh <aws-account-id> <aws-region>

set -e

# Configuration
AWS_ACCOUNT_ID=$1
AWS_REGION=${2:-us-east-1}
ECR_BACKEND_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/face-recognition-backend"
ECR_FRONTEND_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/face-recognition-frontend"
CLUSTER_NAME="face-recognition-cluster"

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "Error: AWS Account ID is required"
    echo "Usage: ./deploy-to-ecs.sh <aws-account-id> [aws-region]"
    exit 1
fi

echo "========================================="
echo "Face Recognition App - ECS Deployment"
echo "========================================="
echo "AWS Account: $AWS_ACCOUNT_ID"
echo "AWS Region: $AWS_REGION"
echo ""

# Step 1: Authenticate Docker to ECR
echo "[1/6] Authenticating Docker to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Step 2: Build Backend Image
echo "[2/6] Building backend Docker image..."
cd backend
docker build -t face-recognition-backend .
docker tag face-recognition-backend:latest $ECR_BACKEND_REPO:latest
cd ..

# Step 3: Build Frontend Image
echo "[3/6] Building frontend Docker image..."
cd frontend
docker build -t face-recognition-frontend .
docker tag face-recognition-frontend:latest $ECR_FRONTEND_REPO:latest
cd ..

# Step 4: Push Images to ECR
echo "[4/6] Pushing backend image to ECR..."
docker push $ECR_BACKEND_REPO:latest

echo "[5/6] Pushing frontend image to ECR..."
docker push $ECR_FRONTEND_REPO:latest

# Step 6: Update ECS Services
echo "[6/6] Updating ECS services..."
aws ecs update-service --cluster $CLUSTER_NAME --service backend-service --force-new-deployment --region $AWS_REGION
aws ecs update-service --cluster $CLUSTER_NAME --service frontend-service --force-new-deployment --region $AWS_REGION

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Check ECS console for deployment status"
echo "2. Monitor CloudWatch logs"
echo "3. Access your application via the Load Balancer URL"
echo ""
