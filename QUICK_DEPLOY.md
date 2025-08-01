# 🚀 Quick Deploy Guide - Microcap Quant

Deploy your AI-powered microcap trading bot in 5 minutes!

## 📋 Prerequisites

Before deploying, you need these API keys:

### 🔑 Required API Keys

1. **OpenAI API Key** (Required)
   - Go to [platform.openai.com](https://platform.openai.com)
   - Create account → API Keys → Create new key
   - Copy the key (starts with `sk-`)

2. **Alpaca Trading API Keys** (Required)
   - Go to [alpaca.markets](https://alpaca.markets)
   - Create account → Paper Trading → API Keys
   - Copy both API Key and Secret Key

### 🔑 Optional API Keys

3. **Anthropic API Key** (Backup AI)
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Create account → API Keys → Create new key

4. **Groq API Key** (Fast inference backup)
   - Go to [console.groq.com](https://console.groq.com)
   - Create account → API Keys → Create new key

## 🚀 Deployment Options

### Option 1: Automated Setup (Recommended)

Run the deployment script:

```bash
python deploy.py
```

This will:
- ✅ Check Python version
- ✅ Create .env file with your API keys
- ✅ Install dependencies
- ✅ Create necessary directories
- ✅ Run basic tests
- ✅ Guide you through deployment options

### Option 2: Railway Deployment (Zero Maintenance)

1. **Fork this repository** to your GitHub account

2. **Go to [Railway.app](https://railway.app)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked repository

3. **Add Environment Variables**
   - Click on your project
   - Go to "Variables" tab
   - Add these variables from your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-key
   ALPACA_API_KEY=your-alpaca-key
   ALPACA_SECRET_KEY=your-alpaca-secret
   PAPER_TRADING=true
   STARTING_CASH=1000
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Bot runs daily at 4:30 PM EST
   - Zero maintenance required

### Option 3: Render Deployment

1. **Go to [Render.com](https://render.com)**
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `microcap-quant`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m auto_trader.automated_trader`
   - **Plan**: Free (or paid for more resources)

3. **Add Environment Variables**
   - Same variables as Railway above

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Option 4: Local Docker

```bash
# Build Docker image
docker build -t microcap-quant .

# Run container
docker run -d --name microcap-quant-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  microcap-quant
```

### Option 5: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp config/.env.example .env
# Edit .env with your keys

# Run the bot
python -m auto_trader.automated_trader
```

## ⚙️ Configuration

### Key Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PAPER_TRADING` | `true` | Set to `false` for live trading |
| `STARTING_CASH` | `1000` | Initial capital in USD |
| `MAX_POSITION_PCT` | `0.15` | Max 15% per stock |
| `STOP_LOSS_PCT` | `0.15` | 15% stop loss |
| `AI_PRIMARY_MODEL` | `gpt-4o` | AI model for decisions |

### Trading Schedule

- **09:30 EST**: Deep research (o3 model)
- **16:30 EST**: Daily trading decisions (GPT-4o)
- **Weekdays only**: Monday-Friday

## 🛡️ Safety Features

- **Paper Trading Default**: Always starts in simulation mode
- **Stop Losses**: Automatic 15% protection on all positions
- **Position Limits**: Maximum 15% per stock
- **Circuit Breaker**: Stops trading if daily loss > 5%
- **Risk Management**: Advanced position sizing and sector limits

## 📊 Monitoring

### Check Bot Status

- **Railway**: Dashboard shows service status
- **Render**: Dashboard shows deployment status
- **Local**: Check logs in `logs/` directory

### View Performance

- **Portfolio**: Check `data/chatgpt_portfolio_update.csv`
- **Trade Log**: Check `data/chatgpt_trade_log.csv`
- **Reports**: Generated in `reports/` directory

### Emergency Stop

- **Railway/Render**: Pause service in dashboard
- **Docker**: `docker stop microcap-quant-bot`
- **Local**: `Ctrl+C` or kill process

## 🚨 Going Live

When ready for real money:

1. **Set `PAPER_TRADING=false`** in environment variables
2. **Get live Alpaca API keys** (not paper keys)
3. **Restart the service**
4. **Monitor first few trades closely**
5. **Start with small capital**

## 💰 Costs

- **Railway**: Free tier or $5/month
- **Render**: Free tier or $7/month
- **OpenAI**: ~$1-5/month (depending on usage)
- **Alpaca**: Free for paper trading, $9/month for live

## 🆘 Troubleshooting

### Bot Not Trading?

1. Check service logs for errors
2. Verify all API keys are correct
3. Ensure cron schedule is set (Railway/Render)
4. Check if market is open (weekdays 9:30-16:00 EST)

### API Errors?

1. Verify API keys are valid
2. Check API usage limits
3. Ensure sufficient credits/balance

### Need Help?

1. Check the logs first
2. Review error messages
3. All activity is logged for debugging

---

**⚠️ Disclaimer**: This software is for educational purposes. Trading involves risk of loss. Use at your own discretion.

**🎉 Ready to deploy?** Run `python deploy.py` to get started! 