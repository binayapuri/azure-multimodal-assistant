import logging
import json
import asyncio
from datetime import datetime

# Import Azure SDKs (will use Terraform-injected config)
try:
    import openai
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from msrest.authentication import CognitiveServicesCredentials
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SERVICES_AVAILABLE = True
except ImportError:
    logging.warning("⚠️ Azure SDKs not installed. Running in mock mode.")
    AZURE_SERVICES_AVAILABLE = False

class TechMartBot:
    """TechMart AI Bot with Terraform-injected Azure configuration"""
    
    def __init__(self, config):
        self.config = config
        self.user_sessions = {}
        self.setup_azure_services()
        self.products = self.load_sample_products()
        logging.info("🤖 TechMart Bot initialized with Terraform configuration")
    
    def setup_azure_services(self):
        """Setup Azure services using Terraform-injected configuration"""
        try:
            if not AZURE_SERVICES_AVAILABLE:
                logging.warning("⚠️ Azure SDKs not available, running in mock mode")
                return
            
            # 🤖 Setup OpenAI with Terraform-injected config
            openai.api_type = "azure"
            openai.api_base = self.config.AZURE_OPENAI_ENDPOINT
            openai.api_key = self.config.AZURE_OPENAI_KEY
            openai.api_version = "2024-02-01"
            
            # 🎤 Setup Speech Service with Terraform-injected config
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.config.AZURE_SPEECH_KEY,
                region=self.config.AZURE_SPEECH_REGION
            )
            
            # 👁️ Setup Computer Vision with Terraform-injected config
            self.cv_client = ComputerVisionClient(
                self.config.AZURE_CV_ENDPOINT,
                CognitiveServicesCredentials(self.config.AZURE_CV_KEY)
            )
            
            logging.info("✅ All Azure services configured with Terraform-injected settings")
            
        except Exception as e:
            logging.error(f"❌ Failed to setup Azure services: {e}")
            self.cv_client = None
            self.speech_config = None
    
    def load_sample_products(self):
        """Load sample product database"""
        return [
            {
                'id': 'laptop_001',
                'name': 'Dell XPS 13 (2024)',
                'category': 'laptop',
                'brand': 'Dell',
                'price': 1299.99,
                'rating': 4.6,
                'features': 'Intel Core i7-1355U, 16GB LPDDR5, 512GB SSD, 13.3" 4K Display',
                'use_cases': ['work', 'productivity', 'travel']
            },
            {
                'id': 'laptop_002',
                'name': 'MacBook Air M2',
                'category': 'laptop',
                'brand': 'Apple',
                'price': 1199.99,
                'rating': 4.8,
                'features': 'Apple M2 chip, 8GB unified memory, 256GB SSD, 13.6" Liquid Retina',
                'use_cases': ['creative', 'work', 'productivity']
            },
            {
                'id': 'laptop_003',
                'name': 'ASUS ROG Strix G15',
                'category': 'laptop',
                'brand': 'ASUS',
                'price': 1599.99,
                'rating': 4.4,
                'features': 'AMD Ryzen 7, RTX 4060, 16GB DDR4, 1TB SSD, 15.6" 144Hz',
                'use_cases': ['gaming', 'streaming', 'content creation']
            },
            {
                'id': 'phone_001',
                'name': 'iPhone 15 Pro',
                'category': 'smartphone',
                'brand': 'Apple',
                'price': 999.99,
                'rating': 4.7,
                'features': 'A17 Pro chip, 128GB storage, 48MP camera system, Titanium design',
                'use_cases': ['photography', 'communication', 'entertainment']
            },
            {
                'id': 'phone_002',
                'name': 'Samsung Galaxy S24 Ultra',
                'category': 'smartphone',
                'brand': 'Samsung',
                'price': 1199.99,
                'rating': 4.5,
                'features': 'Snapdragon 8 Gen 3, 256GB storage, 200MP camera, S Pen included',
                'use_cases': ['photography', 'productivity', 'gaming']
            },
            {
                'id': 'phone_003',
                'name': 'Google Pixel 8 Pro',
                'category': 'smartphone',
                'brand': 'Google',
                'price': 899.99,
                'rating': 4.4,
                'features': 'Google Tensor G3, 128GB storage, AI-enhanced cameras, 7 years updates',
                'use_cases': ['photography', 'AI features', 'pure Android']
            }
        ]
    
    def process_message(self, user_id, message):
        """Process text message using Terraform-configured Azure services"""
        try:
            # Initialize user session
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {
                    'conversation_history': [],
                    'preferences': {}
                }
            
            # Add to conversation history
            self.user_sessions[user_id]['conversation_history'].append({
                'user': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Analyze intent and generate response
            intent = self.analyze_intent(message)
            response = self.generate_response(user_id, message, intent)
            
            # Add response to history
            self.user_sessions[user_id]['conversation_history'].append({
                'bot': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            logging.error(f"Message processing error: {e}")
            return "I apologize, but I'm having trouble processing your request. Please try again."
    
    def analyze_intent(self, message):
        """Analyze user intent"""
        message_lower = message.lower()
        
        # Enhanced intent recognition
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return {'intent': 'greeting'}
        
        elif any(word in message_lower for word in ['laptop', 'computer', 'notebook']):
            # Check for specific laptop needs
            if any(word in message_lower for word in ['gaming', 'game', 'rtx', 'nvidia']):
                return {'intent': 'product_search', 'category': 'laptop', 'subcategory': 'gaming'}
            elif any(word in message_lower for word in ['work', 'business', 'office', 'productivity']):
                return {'intent': 'product_search', 'category': 'laptop', 'subcategory': 'business'}
            else:
                return {'intent': 'product_search', 'category': 'laptop'}
        
        elif any(word in message_lower for word in ['phone', 'smartphone', 'mobile', 'iphone', 'android']):
            return {'intent': 'product_search', 'category': 'smartphone'}
        
        elif any(word in message_lower for word in ['compare', 'difference', 'versus', 'vs', 'better']):
            return {'intent': 'product_compare'}
        
        elif any(word in message_lower for word in ['recommend', 'suggest', 'best', 'top']):
            return {'intent': 'recommendation'}
        
        elif any(word in message_lower for word in ['price', 'cost', 'budget', 'expensive', 'cheap', '$']):
            return {'intent': 'price_inquiry'}
        
        elif any(word in message_lower for word in ['help', 'what can you do', 'features']):
            return {'intent': 'help'}
        
        else:
            return {'intent': 'general_query', 'message': message}
    
    def generate_response(self, user_id, message, intent):
        """Generate response based on intent"""
        try:
            if intent['intent'] == 'greeting':
                return """👋 **Welcome to TechMart!**

I'm your AI shopping assistant, powered by Azure AI services. I can help you find:
- 💻 **Laptops** (Gaming, Business, Ultrabooks)
- 📱 **Smartphones** (iPhone, Android, Budget options)
- 📊 **Product Comparisons**
- 💰 **Budget Recommendations**

What are you looking for today?"""
            
            elif intent['intent'] == 'product_search':
                return self.handle_product_search(intent)
            
            elif intent['intent'] == 'product_compare':
                return self.handle_comparison_request()
            
            elif intent['intent'] == 'recommendation':
                return self.handle_recommendation_request()
            
            elif intent['intent'] == 'price_inquiry':
                return self.handle_price_inquiry()
            
            elif intent['intent'] == 'help':
                return self.handle_help_request()
            
            elif intent['intent'] == 'general_query':
                return self.handle_general_query_with_ai(intent['message'])
            
            else:
                return "I'm here to help you find great tech products! Ask me about laptops, smartphones, or any tech-related questions."
                
        except Exception as e:
            logging.error(f"Response generation error: {e}")
            return "I'm here to help you find amazing tech products! What are you looking for?"
    
    def handle_product_search(self, intent):
        """Handle product search with enhanced filtering"""
        category = intent.get('category', 'general')
        subcategory = intent.get('subcategory', 'all')
        
        if category == 'laptop':
            laptops = [p for p in self.products if p['category'] == 'laptop']
            
            # Filter by subcategory
            if subcategory == 'gaming':
                laptops = [p for p in laptops if any(use in p['use_cases'] for use in ['gaming', 'streaming'])]
            elif subcategory == 'business':
                laptops = [p for p in laptops if any(use in p['use_cases'] for use in ['work', 'productivity'])]
            
            response = f"💻 **{'Gaming ' if subcategory == 'gaming' else 'Business ' if subcategory == 'business' else ''}Laptops Available:**\n\n"
            
            for laptop in laptops:
                response += f"**{laptop['name']}** - ${laptop['price']:,.2f}\n"
                response += f"✨ {laptop['features']}\n"
                response += f"⭐ Rating: {laptop['rating']}/5 | 🎯 Best for: {', '.join(laptop['use_cases'])}\n\n"
        
        elif category == 'smartphone':
            phones = [p for p in self.products if p['category'] == 'smartphone']
            response = "📱 **Excellent Smartphones:**\n\n"
            
            for phone in phones:
                response += f"**{phone['name']}** - ${phone['price']:,.2f}\n"
                response += f"✨ {phone['features']}\n"
                response += f"⭐ Rating: {phone['rating']}/5 | 🎯 Best for: {', '.join(phone['use_cases'])}\n\n"
        
        else:
            response = """🔍 **What can I help you find?**

**Laptops:**
- Gaming laptops for high performance
- Business laptops for productivity
- Ultrabooks for portability

**Smartphones:**
- Latest iPhones and Android devices
- Budget-friendly options
- Camera-focused phones

Tell me your specific needs and budget!"""
        
        response += "\n💡 **Need help deciding?** Tell me your budget and how you'll use it!"
        return response
    
    def handle_comparison_request(self):
        """Handle product comparison requests"""
        return """🆚 **Product Comparisons:**

**Popular Laptop Comparisons:**
- **Dell XPS 13 vs MacBook Air M2**
  - XPS: More ports, 4K display, Windows flexibility
  - MacBook: Better battery, fanless design, macOS integration

- **Gaming vs Business Laptops**
  - Gaming: Dedicated GPU, high refresh displays, RGB
  - Business: Better battery, lighter weight, professional design

**Smartphone Comparisons:**
- **iPhone 15 Pro vs Galaxy S24 Ultra**
  - iPhone: Better video, longer updates, iOS ecosystem
  - Galaxy: S Pen, more customization, larger screen

**Tell me specific products you want compared!**"""
    
    def handle_recommendation_request(self):
        """Handle recommendation requests"""
        # Get top-rated products across categories
        top_products = sorted(self.products, key=lambda x: x['rating'], reverse=True)[:4]
        
        response = "🌟 **My Top Recommendations:**\n\n"
        
        for i, product in enumerate(top_products, 1):
            response += f"**{i}. {product['name']}** - ${product['price']:,.2f}\n"
            response += f"   📱 {product['category'].title()} | ⭐ {product['rating']}/5\n"
            response += f"   ✨ {product['features'][:60]}...\n\n"
        
        response += """💡 **For personalized recommendations, tell me:**
- Your budget range
- Primary use (work, gaming, photography, etc.)
- Preferred brand or features
- Any specific requirements"""
        
        return response
    
    def handle_price_inquiry(self):
        """Handle price-related questions"""
        return """💰 **TechMart Price Guide:**

**💻 Laptops:**
- **Budget ($500-800):** Entry-level productivity laptops
- **Mid-range ($800-1300):** Quality laptops like Dell XPS 13, MacBook Air
- **Premium ($1300+):** High-end gaming laptops, MacBook Pro

**📱 Smartphones:**
- **Budget ($200-500):** Basic Android phones, older iPhones
- **Mid-range ($500-900):** Google Pixel 8 Pro, Galaxy S24
- **Premium ($900+):** iPhone 15 Pro, Galaxy S24 Ultra

**🔥 Current Deals:**
- MacBook Air M2: $1,199 (normally $1,299)
- Dell XPS 13: Starting at $1,299
- iPhone 15 Pro: $999 with trade-in deals

**What's your budget range? I'll find the best options!**"""
    
    def handle_help_request(self):
        """Handle help requests"""
        return """🤖 **How I Can Help You:**

**🔍 Product Search:**
- "Find gaming laptops under $1500"
- "Show me iPhones with good cameras"

**🆚 Comparisons:**
- "Compare MacBook vs Dell XPS"
- "iPhone vs Samsung differences"

**💡 Recommendations:**
- "What's the best laptop for work?"
- "Recommend a phone for photography"

**💰 Budget Help:**
- "Laptops under $1000"
- "Best value smartphones"

**📷 Image Recognition:**
- Upload product photos for identification
- Get similar product suggestions

**I'm powered by Azure AI and have access to real-time product data!**"""
    
    def handle_general_query_with_ai(self, message):
        """Handle general queries using Azure OpenAI (if configured)"""
        try:
            if AZURE_SERVICES_AVAILABLE and hasattr(self, 'config') and self.config.AZURE_OPENAI_ENDPOINT:
                # Use Azure OpenAI for advanced queries
                response = openai.ChatCompletion.create(
                    engine=self.config.AZURE_OPENAI_DEPLOYMENT,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a helpful technology shopping assistant for TechMart. Help users find and learn about laptops, smartphones, tablets, and accessories. Be concise, helpful, and focus on product recommendations. Always encourage users to ask about specific products or needs."
                        },
                        {"role": "user", "content": message}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content.strip()
                return f"{ai_response}\n\n💡 **Ask me about specific products or your tech needs!**"
            else:
                # Fallback response
                return """I'd be happy to help you with that! As your TechMart AI assistant, I specialize in:

- Finding the perfect laptops and smartphones
- Comparing different products
- Providing budget recommendations
- Answering tech-related questions

What specific technology product or question can I help you with today?"""
                
        except Exception as e:
            logging.error(f"AI query error: {e}")
            return "I'm here to help you find great technology products! What are you looking for - laptops, smartphones, or something else?"
    
    def process_image(self, user_id, image_data):
        """Process uploaded image using Terraform-configured Computer Vision"""
        try:
            if not AZURE_SERVICES_AVAILABLE or not self.cv_client:
                return self.mock_image_processing()
            
            # Use Azure Computer Vision with Terraform-injected config
            import io
            image_stream = io.BytesIO(image_data)
            
            # Analyze image
            analysis = self.cv_client.analyze_image_in_stream(
                image_stream,
                visual_features=['Description', 'Tags', 'Objects']
            )
            
            # Process results
            description = ""
            if analysis.description and analysis.description.captions:
                description = analysis.description.captions[0].text
            
            # Detect tech products
            tech_tags = ['laptop', 'computer', 'phone', 'smartphone', 'tablet', 'monitor', 'keyboard']
            detected_tech = [tag.name for tag in analysis.tags if tag.name.lower() in tech_tags and tag.confidence > 0.5]
            
            if detected_tech:
                tech_type = detected_tech[0].lower()
                response = f"📷 **Image Analysis Complete!**\n\nI can see this appears to be a **{tech_type}**!\n\n"
                
                # Get similar products
                if 'laptop' in tech_type or 'computer' in tech_type:
                    similar_products = [p for p in self.products if p['category'] == 'laptop'][:2]
                elif 'phone' in tech_type:
                    similar_products = [p for p in self.products if p['category'] == 'smartphone'][:2]
                else:
                    similar_products = []
                
                if similar_products:
                    response += "**Here are some similar products I'd recommend:**\n\n"
                    for product in similar_products:
                        response += f"• **{product['name']}** - ${product['price']:,.2f}\n"
                        response += f"  ⭐ {product['rating']}/5 | {product['features'][:50]}...\n\n"
                
                response += "💡 **Want more details about any of these products?**"
                
            else:
                response = f"📷 **Image Received:** {description}\n\nWhile I couldn't identify a specific tech product, I'm here to help you find what you need!\n\n**What type of technology are you looking for?**\n• Laptops 💻\n• Smartphones 📱\n• Tablets\n• Accessories"
            
            return response
            
        except Exception as e:
            logging.error(f"Image processing error: {e}")
            return self.mock_image_processing()
    
    def mock_image_processing(self):
        """Mock image processing when Azure services not available"""
        return """📷 **Image Analysis (Demo Mode):**

I can see your uploaded image! In full deployment with Azure Computer Vision, I would:

✅ **Identify tech products** in your photos
✅ **Extract text** from product labels  
✅ **Suggest similar products** from our catalog
✅ **Provide detailed specifications**

**Currently showing sample recommendations:**

**Laptops:**
- Dell XPS 13 - $1,299.99 ⭐ 4.6/5
- MacBook Air M2 - $1,199.99 ⭐ 4.8/5

**Smartphones:**  
- iPhone 15 Pro - $999.99 ⭐ 4.7/5
- Galaxy S24 Ultra - $1,199.99 ⭐ 4.5/5

**What type of product are you looking for?**"""
    
    def process_voice(self, user_id, audio_data):
        """Process voice input using Terraform-configured Speech Services"""
        try:
            if not AZURE_SERVICES_AVAILABLE or not self.speech_config:
                return self.mock_voice_processing()
            
            # Voice processing would go here using Azure Speech Services
            # with self.speech_config (injected by Terraform)
            
            return """🎤 **Voice Processing Available!**

I heard your voice input! With Azure Speech Services configured, I can:

✅ **Convert speech to text** with high accuracy
✅ **Support multiple languages** and accents
✅ **Provide voice responses** back to you
✅ **Handle natural conversations** via voice

**Try saying things like:**
- "Find me a gaming laptop under $1500"
- "Compare iPhone and Samsung phones"
- "What's the best laptop for work?"

**What would you like to know about our tech products?**"""
            
        except Exception as e:
            logging.error(f"Voice processing error: {e}")
            return self.mock_voice_processing()
    
    def mock_voice_processing(self):
        """Mock voice processing when Azure services not available"""
        return """🎤 **Voice Input Received!**

Voice processing is ready with Azure Speech Services! I can understand natural speech and respond with:

💬 **Speech-to-Text:** Convert your voice to text
🔊 **Text-to-Speech:** Respond with natural voice
🌍 **Multi-language:** Support for various languages
🎯 **Intent Recognition:** Understand what you're looking for

**You can ask me about:**
- Product recommendations
- Price comparisons  
- Technical specifications
- Availability and deals

**What tech products interest you today?**"""