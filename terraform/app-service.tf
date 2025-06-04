# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "techmart-plan-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B2"
  
  tags = azurerm_resource_group.main.tags
}

# ZIP file for application deployment
data "archive_file" "app_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../app"
  output_path = "${path.module}/app.zip"
}

# Storage Blob for application package
resource "azurerm_storage_blob" "app_package" {
  name                   = "app-${random_string.suffix.result}.zip"
  storage_account_name   = azurerm_storage_account.main.name
  storage_container_name = azurerm_storage_container.deployments.name
  type                   = "Block"
  source                 = data.archive_file.app_zip.output_path
}

# Storage Container for deployments
resource "azurerm_storage_container" "deployments" {
  name                  = "deployments"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Generate SAS token for blob access
data "azurerm_storage_account_blob_container_sas" "app_package" {
  connection_string = azurerm_storage_account.main.primary_connection_string
  container_name    = azurerm_storage_container.deployments.name
  https_only        = true

  start  = "2024-01-01T00:00:00Z"
  expiry = "2025-12-31T23:59:59Z"

  permissions {
    read   = true
    add    = false
    create = false
    write  = false
    delete = false
    list   = false
  }
}

# Web App with AUTOMATIC configuration injection
resource "azurerm_linux_web_app" "main" {
  name                = "techmart-bot-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = "3.9"
    }
    always_on = true
  }

  # 🔥 AUTOMATIC CONFIGURATION - All Azure services auto-configured!
  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"     = "true"
    "WEBSITE_RUN_FROM_PACKAGE"            = "https://${azurerm_storage_account.main.name}.blob.core.windows.net/${azurerm_storage_container.deployments.name}/${azurerm_storage_blob.app_package.name}${data.azurerm_storage_account_blob_container_sas.app_package.sas}"
    
    # 🤖 Azure OpenAI - Auto-configured from Terraform
    "AZURE_OPENAI_ENDPOINT"   = azurerm_cognitive_account.openai.endpoint
    "AZURE_OPENAI_KEY"        = azurerm_cognitive_account.openai.primary_access_key
    "AZURE_OPENAI_DEPLOYMENT" = local.openai_deployment_name
    
    # 🎤 Speech Services - Auto-configured from Terraform
    "AZURE_SPEECH_KEY"    = azurerm_cognitive_account.speech.primary_access_key
    "AZURE_SPEECH_REGION" = azurerm_cognitive_account.speech.location
    
    # 👁️ Computer Vision - Auto-configured from Terraform
    "AZURE_CV_ENDPOINT" = azurerm_cognitive_account.vision.endpoint
    "AZURE_CV_KEY"      = azurerm_cognitive_account.vision.primary_access_key
    
    # 🔍 Cognitive Search - Auto-configured from Terraform
    "AZURE_SEARCH_ENDPOINT" = "https://${azurerm_search_service.main.name}.search.windows.net"
    "AZURE_SEARCH_KEY"      = azurerm_search_service.main.primary_key
    "AZURE_SEARCH_INDEX"    = "products-index"
    
    # 🗄️ Cosmos DB - Auto-configured from Terraform
    "AZURE_COSMOS_ENDPOINT"  = azurerm_cosmosdb_account.main.endpoint
    "AZURE_COSMOS_KEY"       = azurerm_cosmosdb_account.main.primary_key
    "AZURE_COSMOS_DATABASE"  = azurerm_cosmosdb_sql_database.main.name
    
    # 📊 Application Insights - Auto-configured from Terraform
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.main.connection_string
    
    # ⚙️ Application Settings
    "PORT"        = "8000"
    "DEBUG"       = "false"
    "ENVIRONMENT" = var.environment
  }

  tags = azurerm_resource_group.main.tags
}