#!/bin/bash

# Google Cloud Run Deployment Script for Clinic Management System
# Make sure you have gcloud CLI installed and authenticated

# Configuration
PROJECT_ID="zospital"
SERVICE_NAME="clinic-management"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting deployment to Google Cloud Run...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if project ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo -e "${RED}❌ Please update PROJECT_ID in this script with your actual Google Cloud Project ID${NC}"
    exit 1
fi

# Set the project
echo -e "${YELLOW}📋 Setting Google Cloud project...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required Google Cloud APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build the Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars "DJANGO_SETTINGS_MODULE=crm.settings" \
    --set-env-vars "DEBUG=False" \
    --set-env-vars "ALLOWED_HOSTS=*" \
    --set-env-vars "SECRET_KEY=your-secret-key-here" \
    --set-env-vars "DATABASE_URL=your-database-url-here"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${GREEN}🌐 Your application is available at: $SERVICE_URL${NC}"
echo -e "${YELLOW}⚠️  Make sure to update the environment variables with your actual values:${NC}"
echo -e "   - SECRET_KEY: Generate a new Django secret key"
echo -e "   - DATABASE_URL: Your PostgreSQL database connection string"
echo -e "   - Any other environment variables from your production.env.example"

echo -e "${YELLOW}📝 To update environment variables later, use:${NC}"
echo -e "gcloud run services update $SERVICE_NAME --region $REGION --set-env-vars KEY=VALUE" 