#!/bin/bash

echo "🚀 TechMart AI Bot - Complete Deployment with Terraform"
echo "======================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform is not installed. Please install Terraform first.${NC}"
    echo "   Install from: https://www.terraform.io/downloads"
    exit 1
fi

if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install Azure CLI first.${NC}"
    echo "   Install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check Azure login
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}🔐 Please log in to Azure...${NC}"
    az login
fi

echo -e "${GREEN}✅ Prerequisites check passed!${NC}"

# Navigate to terraform directory
cd terraform

echo -e "${BLUE}🔧 Initializing Terraform...${NC}"
terraform init

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Terraform initialization failed!${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Planning deployment...${NC}"
terraform plan -out=tfplan

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Terraform planning failed!${NC}"
    exit 1
fi

echo -e "${YELLOW}🚀 Starting deployment to Azure...${NC}"
echo "This will create Azure resources and deploy your application..."
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

echo -e "${BLUE}⚡ Deploying to Azure...${NC}"
terraform apply tfplan

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL!${NC}"
echo "==============================="

# Get outputs
echo -e "${BLUE}📊 Deployment Summary:${NC}"
terraform output -json | jq -r '.deployment_summary.value | to_entries[] | "\(.key): \(.value)"'

echo ""
echo -e "${GREEN}✅ $(terraform output -raw configuration_injected)${NC}"

echo ""
echo -e "${YELLOW}🌐 Your TechMart AI Bot is now live at:${NC}"
echo -e "${GREEN}$(terraform output -raw web_app_url)${NC}"

echo ""
echo -e "${BLUE}🔧 What was automatically configured:${NC}"
echo "   🤖 Azure OpenAI (GPT-4) - Ready for AI conversations"
echo "   🎤 Speech Services - Voice input/output ready"
echo "   👁️ Computer Vision - Image analysis ready" 
echo "   🔍 Cognitive Search - Product search ready"
echo "   🗄️ Cosmos DB - Data storage ready"
echo "   📊 Application Insights - Monitoring ready"

echo ""
echo -e "${GREEN}🎯 Next Steps:${NC}"
echo "   1. Visit your bot URL to start chatting"
echo "   2. Test text, image, and voice features"
echo "   3. Monitor performance in Azure Portal"

echo ""
echo -e "${YELLOW}🗑️ To remove all resources when done:${NC}"
echo "   cd terraform && terraform destroy"

echo ""
echo -e "${GREEN}🚀 Enjoy your AI-powered TechMart assistant!${NC}"