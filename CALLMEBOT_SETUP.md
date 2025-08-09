# CallMeBot WhatsApp API Setup Guide

## 📱 Complete Setup for +905525242866

Follow these exact steps to enable automatic WhatsApp notifications:

### Step 1: Add CallMeBot Contact
1. Open WhatsApp on your phone (+905525242866)
2. Add this number to your contacts: **+34 684 73 40 44**
3. Name it: "CallMeBot" (or any name you prefer)

### Step 2: Activate API
1. Send this exact message to the CallMeBot contact:
   ```
   I allow callmebot to send me messages
   ```
2. Wait for the API activation message (usually within 2 minutes)
3. You'll receive: "API Activated for your phone number. Your APIKEY is XXXXXXX"

### Step 3: Configure the Application
1. Create/edit the `.env` file in the project root
2. Add this line with your received API key:
   ```
   CALLMEBOT_API_KEY=your_received_api_key_here
   ```

### Step 4: Test the Setup
1. Restart the Flask application
2. Visit: http://127.0.0.1:5000/admin/test-whatsapp
3. Or submit a real lead form

## ✅ Once Configured:
- Every lead form submission will automatically send a WhatsApp message
- Messages go directly to +905525242866
- Includes all lead information: name, phone, email, preferences, etc.
- Professional formatting with emojis and structured data

## 🔧 Troubleshooting:
- If no API key received in 2 minutes, try again after 24 hours
- Make sure you send the exact message: "I allow callmebot to send me messages"
- The bot contact must be +34 684 73 40 44
- API key should be numbers only (e.g., 123456789)

## 📞 Support:
- CallMeBot Support: support@callmebot.com
- Telegram: @callmebot_com

## 🚨 Important:
The free API is for personal use only. Perfect for real estate lead notifications!
