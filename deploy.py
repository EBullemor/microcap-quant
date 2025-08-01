#!/usr/bin/env python3
"""
Microcap Quant Deployment Script
Automates the deployment process for the AI trading bot
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print deployment banner"""
    print("=" * 60)
    print("🚀 MICROCAP QUANT - DEPLOYMENT SCRIPT")
    print("=" * 60)
    print("AI-Powered Microcap Trading Bot")
    print("Version: 0.2.0")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Error: Python 3.9+ required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_env_file():
    """Create .env file with user input"""
    env_template = """# =============================================================================
# MICROCAP QUANT - ENVIRONMENT VARIABLES
# =============================================================================

# =============================================================================
# AI API KEYS (Required)
# =============================================================================

# OpenAI API Key (Required for GPT-4o and o3 deep research)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY={openai_key}

# Anthropic API Key (Optional - backup AI provider)
# Get from: https://console.anthropic.com/
ANTHROPIC_API_KEY={anthropic_key}

# Groq API Key (Optional - fast inference backup)
# Get from: https://console.groq.com/
GROQ_API_KEY={groq_key}

# =============================================================================
# TRADING API KEYS (Required)
# =============================================================================

# Alpaca Trading API Keys
# Get from: https://alpaca.markets/ (Paper Trading for testing)
ALPACA_API_KEY={alpaca_key}
ALPACA_SECRET_KEY={alpaca_secret}

# =============================================================================
# AI MODEL CONFIGURATION
# =============================================================================

# Primary AI model for daily decisions (16:30 EST cycle)
AI_PRIMARY_MODEL=gpt-4o

# Backup AI model if primary fails
AI_BACKUP_MODEL=gpt-4

# Deep research model for pre-market analysis (09:30 EST cycle)
AI_RESEARCH_MODEL=o3-deep-research-2025-06-26

# =============================================================================
# TRADING CONFIGURATION
# =============================================================================

# Set to false for live trading (default: true for safety)
PAPER_TRADING=true

# Starting capital in USD
STARTING_CASH={starting_cash}

# Maximum position size as percentage (0.15 = 15%)
MAX_POSITION_PCT=0.15

# Stop loss percentage (0.15 = 15%)
STOP_LOSS_PCT=0.15

# Maximum daily loss before circuit breaker (0.05 = 5%)
MAX_DAILY_LOSS=0.05

# =============================================================================
# NOTIFICATIONS (Optional)
# =============================================================================

# Slack webhook for alerts
SLACK_WEBHOOK={slack_webhook}

# Email notifications (requires SMTP setup)
EMAIL_ALERTS=false
EMAIL_FROM={email_from}
EMAIL_TO={email_to}
EMAIL_PASSWORD={email_password}

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================

# Market cap maximum for microcap universe ($300M default)
MARKET_CAP_MAX=300000000

# Minimum daily volume filter ($50K default)
MIN_VOLUME=50000

# Timezone for trading schedules
TIMEZONE=US/Eastern

# Data directory for portfolio and trade logs
DATA_DIR=data
"""
    
    print("\n🔑 API KEY SETUP")
    print("=" * 40)
    
    # Get API keys from user
    openai_key = input("Enter your OpenAI API key (sk-...): ").strip()
    if not openai_key.startswith("sk-"):
        print("⚠️  Warning: OpenAI key should start with 'sk-'")
    
    anthropic_key = input("Enter your Anthropic API key (optional, sk-ant-...): ").strip()
    groq_key = input("Enter your Groq API key (optional, gsk-...): ").strip()
    
    alpaca_key = input("Enter your Alpaca API key: ").strip()
    alpaca_secret = input("Enter your Alpaca Secret key: ").strip()
    
    # Trading configuration
    print("\n💰 TRADING CONFIGURATION")
    print("=" * 40)
    
    starting_cash = input("Starting capital (default: 1000): ").strip() or "1000"
    
    # Notifications
    print("\n📧 NOTIFICATIONS (Optional)")
    print("=" * 40)
    
    slack_webhook = input("Slack webhook URL (optional): ").strip() or ""
    email_from = input("Email for notifications (optional): ").strip() or ""
    email_to = input("Email to receive reports (optional): ").strip() or ""
    email_password = input("Email app password (optional): ").strip() or ""
    
    # Create .env file
    env_content = env_template.format(
        openai_key=openai_key,
        anthropic_key=anthropic_key,
        groq_key=groq_key,
        alpaca_key=alpaca_key,
        alpaca_secret=alpaca_secret,
        starting_cash=starting_cash,
        slack_webhook=slack_webhook,
        email_from=email_from,
        email_to=email_to,
        email_password=email_password
    )
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env file created successfully")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 INSTALLING DEPENDENCIES")
    print("=" * 40)
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def run_tests():
    """Run basic tests to verify setup"""
    print("\n🧪 RUNNING TESTS")
    print("=" * 40)
    
    try:
        # Test AI connection
        result = subprocess.run([sys.executable, "tests/test_ai_only.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ AI connection test passed")
        else:
            print("⚠️  AI test failed - check your API keys")
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"⚠️  Test failed: {e}")

def create_directories():
    """Create necessary directories"""
    print("\n📁 CREATING DIRECTORIES")
    print("=" * 40)
    
    directories = ["data", "logs", "reports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/")

def show_deployment_options():
    """Show deployment options"""
    print("\n🚀 DEPLOYMENT OPTIONS")
    print("=" * 40)
    print("1. Railway (Recommended - Zero maintenance)")
    print("2. Render (Alternative cloud platform)")
    print("3. Local Docker")
    print("4. Local Python")
    
    choice = input("\nSelect deployment option (1-4): ").strip()
    
    if choice == "1":
        deploy_railway()
    elif choice == "2":
        deploy_render()
    elif choice == "3":
        deploy_docker()
    elif choice == "4":
        deploy_local()
    else:
        print("Invalid choice. Exiting.")

def deploy_railway():
    """Deploy to Railway"""
    print("\n🚂 RAILWAY DEPLOYMENT")
    print("=" * 40)
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Login: railway login")
    print("3. Deploy: railway up")
    print("\nOr use the web interface:")
    print("1. Go to https://railway.app")
    print("2. Connect your GitHub repository")
    print("3. Add environment variables from .env file")
    print("4. Deploy!")

def deploy_render():
    """Deploy to Render"""
    print("\n🎨 RENDER DEPLOYMENT")
    print("=" * 40)
    print("1. Go to https://render.com")
    print("2. Connect your GitHub repository")
    print("3. Create a new Web Service")
    print("4. Add environment variables from .env file")
    print("5. Set build command: pip install -r requirements.txt")
    print("6. Set start command: python -m auto_trader.automated_trader")

def deploy_docker():
    """Deploy using Docker"""
    print("\n🐳 DOCKER DEPLOYMENT")
    print("=" * 40)
    
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker detected")
        
        # Build and run Docker container
        subprocess.run(["docker", "build", "-t", "microcap-quant", "."], check=True)
        print("✅ Docker image built")
        
        # Run container
        subprocess.run([
            "docker", "run", "-d", "--name", "microcap-quant-bot",
            "--env-file", ".env",
            "-v", f"{os.getcwd()}/data:/app/data",
            "microcap-quant"
        ], check=True)
        print("✅ Docker container started")
        
    except subprocess.CalledProcessError:
        print("❌ Docker not available or failed")
        print("Install Docker from https://docker.com")

def deploy_local():
    """Deploy locally"""
    print("\n💻 LOCAL DEPLOYMENT")
    print("=" * 40)
    
    # Create systemd service file
    service_content = """[Unit]
Description=Microcap Quant Trading Bot
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={cwd}
Environment=PATH={cwd}/venv/bin
ExecStart={cwd}/venv/bin/python -m auto_trader.automated_trader
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
""".format(user=os.getenv("USER"), cwd=os.getcwd())
    
    with open("microcap-quant.service", "w") as f:
        f.write(service_content)
    
    print("✅ Systemd service file created: microcap-quant.service")
    print("\nTo start the service:")
    print("sudo cp microcap-quant.service /etc/systemd/system/")
    print("sudo systemctl enable microcap-quant")
    print("sudo systemctl start microcap-quant")

def main():
    """Main deployment function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Run tests
    run_tests()
    
    # Show deployment options
    show_deployment_options()
    
    print("\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 40)
    print("Your Microcap Quant bot is ready to trade!")
    print("\n📊 Monitor your bot:")
    print("- Check logs in logs/ directory")
    print("- View portfolio in data/ directory")
    print("- Review performance reports")
    
    print("\n⚠️  IMPORTANT:")
    print("- Bot starts in PAPER TRADING mode for safety")
    print("- Set PAPER_TRADING=false in .env for live trading")
    print("- Monitor first few trades closely")
    print("- All trades are logged for review")

if __name__ == "__main__":
    main() 