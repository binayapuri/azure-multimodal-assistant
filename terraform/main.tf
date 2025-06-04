terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.1"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Random suffix for unique names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "techmart-bot-${random_string.suffix.result}"
  location = var.location
  
  tags = {
    Environment = var.environment
    Project     = "techmart-ai-bot"
    Owner       = "binaya-puri"
  }
}

# Azure OpenAI Service
resource "azurerm_cognitive_account" "openai" {
  name                = "techmart-openai-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = azurerm_resource_group.main.tags
}

# Note: Model deployment will be done via Azure Portal or CLI after resource creation
# This avoids Terraform provider version compatibility issues
locals {
  openai_deployment_name = "gpt-4-turbo"
}

# Speech Services
resource "azurerm_cognitive_account" "speech" {
  name                = "techmart-speech-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "SpeechServices"
  sku_name            = "S0"

  tags = azurerm_resource_group.main.tags
}

# Computer Vision
resource "azurerm_cognitive_account" "vision" {
  name                = "techmart-vision-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "ComputerVision"
  sku_name            = "S1"

  tags = azurerm_resource_group.main.tags
}

# Cognitive Search
resource "azurerm_search_service" "main" {
  name                = "techmart-search-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "basic"

  tags = azurerm_resource_group.main.tags
}

# Cosmos DB
resource "azurerm_cosmosdb_account" "main" {
  name                = "techmart-cosmos-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }

  tags = azurerm_resource_group.main.tags
}

# Cosmos DB Database
resource "azurerm_cosmosdb_sql_database" "main" {
  name                = "techmart"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "techmart${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = azurerm_resource_group.main.tags
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = "techmart-insights-${random_string.suffix.result}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"

  tags = azurerm_resource_group.main.tags
}