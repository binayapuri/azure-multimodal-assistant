output "web_app_url" {
  description = "URL of the deployed TechMart AI Bot"
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "deployment_summary" {
  description = "Summary of all deployed resources and their endpoints"
  value = {
    "🌐 Application URL"     = "https://${azurerm_linux_web_app.main.default_hostname}"
    "🤖 OpenAI Endpoint"     = azurerm_cognitive_account.openai.endpoint
    "🎤 Speech Region"       = azurerm_cognitive_account.speech.location
    "👁️ Vision Endpoint"     = azurerm_cognitive_account.vision.endpoint
    "🔍 Search Endpoint"     = "https://${azurerm_search_service.main.name}.search.windows.net"
    "🗄️ Cosmos Endpoint"     = azurerm_cosmosdb_account.main.endpoint
    "📊 App Insights"        = azurerm_application_insights.main.app_id
    "📁 Resource Group"      = azurerm_resource_group.main.name
  }
}

output "configuration_injected" {
  description = "Confirmation that all configuration has been automatically injected"
  value = "✅ All Azure service configurations have been automatically injected into the application!"
}