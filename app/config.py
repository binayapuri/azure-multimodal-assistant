import os
import logging

class Config:
    """Configuration class that automatically receives Terraform-injected settings"""
    
    def __init__(self):
        self.load_terraform_config()
        self.validate_config()
        logging.info("✅ Configuration loaded from Terraform-injected environment variables")
    
    def load_terraform_config(self):
        """Load configuration automatically injected by Terraform"""
        
        # 🤖 Azure OpenAI (Auto-injected by Terraform)
        self.AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
        self.AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
        
        # 🎤 Azure Speech Services (Auto-injected by Terraform)
        self.AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
        self.AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION')
        
        # 👁️ Azure Computer Vision (Auto-injected by Terraform)
        self.AZURE_CV_ENDPOINT = os.getenv('AZURE_CV_ENDPOINT')
        self.AZURE_CV_KEY = os.getenv('AZURE_CV_KEY')
        
        # 🔍 Azure Cognitive Search (Auto-injected by Terraform)
        self.AZURE_SEARCH_ENDPOINT = os.getenv('AZURE_SEARCH_ENDPOINT')
        self.AZURE_SEARCH_KEY = os.getenv('AZURE_SEARCH_KEY')
        self.AZURE_SEARCH_INDEX = os.getenv('AZURE_SEARCH_INDEX', 'products-index')
        
        # 🗄️ Azure Cosmos DB (Auto-injected by Terraform)
        self.AZURE_COSMOS_ENDPOINT = os.getenv('AZURE_COSMOS_ENDPOINT')
        self.AZURE_COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')
        self.AZURE_COSMOS_DATABASE = os.getenv('AZURE_COSMOS_DATABASE', 'techmart')
        
        # 📊 Application Insights (Auto-injected by Terraform)
        self.APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
        
        # ⚙️ Application Settings (Auto-injected by Terraform)
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        self.PORT = int(os.getenv('PORT', 8000))
        
        logging.info(f"🌐 Environment: {self.ENVIRONMENT}")
        logging.info(f"🔧 Debug mode: {self.DEBUG}")
    
    def validate_config(self):
        """Validate that Terraform properly injected the configuration"""
        required_settings = [
            ('AZURE_OPENAI_ENDPOINT', self.AZURE_OPENAI_ENDPOINT),
            ('AZURE_OPENAI_KEY', self.AZURE_OPENAI_KEY),
            ('AZURE_SPEECH_KEY', self.AZURE_SPEECH_KEY),
            ('AZURE_SPEECH_REGION', self.AZURE_SPEECH_REGION),
            ('AZURE_CV_ENDPOINT', self.AZURE_CV_ENDPOINT),
            ('AZURE_CV_KEY', self.AZURE_CV_KEY)
        ]
        
        missing_settings = []
        for setting_name, setting_value in required_settings:
            if not setting_value or setting_value == 'mock':
                missing_settings.append(setting_name)
        
        if missing_settings:
            error_msg = f"❌ Terraform failed to inject required configuration: {', '.join(missing_settings)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        logging.info("✅ All required configuration successfully injected by Terraform")
    
    def get_service_status(self):
        """Get status of all configured services"""
        return {
            'openai_configured': bool(self.AZURE_OPENAI_ENDPOINT and self.AZURE_OPENAI_KEY),
            'speech_configured': bool(self.AZURE_SPEECH_KEY),
            'vision_configured': bool(self.AZURE_CV_ENDPOINT and self.AZURE_CV_KEY),
            'search_configured': bool(self.AZURE_SEARCH_ENDPOINT),
            'cosmos_configured': bool(self.AZURE_COSMOS_ENDPOINT),
            'insights_configured': bool(self.APPLICATIONINSIGHTS_CONNECTION_STRING)
        }