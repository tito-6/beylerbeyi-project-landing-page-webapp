# 🚀 Hostinger Deployment - Quick Guide

## 1️⃣ **CHOOSE HOSTING (IMPORTANT!)**
- ❌ **Shared Hosting** - NO Python support
- ✅ **VPS Hosting** - Best choice ($3.99/month+)
- ✅ **Cloud Hosting** - More expensive ($9.99/month+)

## 2️⃣ **PURCHASE & SETUP**
1. Go to hostinger.com
2. Buy VPS Hosting (minimum 1GB RAM)
3. Wait for setup email with server details

## 3️⃣ **QUICK SSH COMMANDS**
```bash
# Connect to server
ssh root@your-server-ip

# Install everything needed
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv nginx supervisor git -y

# Upload your files
cd /var/www
git clone https://github.com/your-username/estate-vue.git
cd estate-vue

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create environment file
echo "SESSION_SECRET=your-super-secret-key-change-this-32-chars
CALLMEBOT_API_KEY=9250107
FLASK_ENV=production" > .env
```

## 4️⃣ **CONFIGURE SERVICES**

### Create Supervisor Config:
```bash
cat > /etc/supervisor/conf.d/estate-vue.conf << 'EOF'
[program:estate-vue]
directory=/var/www/estate-vue
command=/var/www/estate-vue/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 app:app
autostart=true
autorestart=true
stderr_logfile=/var/log/estate-vue.err.log
stdout_logfile=/var/log/estate-vue.out.log
user=root
EOF
```

### Create Nginx Config:
```bash
cat > /etc/nginx/sites-available/estate-vue << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/estate-vue/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/estate-vue /etc/nginx/sites-enabled/
```

## 5️⃣ **START EVERYTHING**
```bash
# Start services
systemctl restart supervisor nginx
systemctl enable supervisor nginx

# Check status
supervisorctl status
systemctl status nginx
```

## 6️⃣ **POINT DOMAIN**
1. Hostinger Control Panel → DNS Zone
2. A Record: @ → Your VPS IP
3. A Record: www → Your VPS IP

## 7️⃣ **ENABLE HTTPS**
```bash
# Install SSL
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com -d www.your-domain.com
```

## 🎯 **TEST YOUR SITE**
1. Visit: https://your-domain.com
2. Submit test lead → Check WhatsApp +905525242866
3. Test "Ara Beni" button
4. Try all languages: /en, /tr, /ar

## 🛠️ **USEFUL COMMANDS**
```bash
# Check logs
tail -f /var/log/estate-vue.out.log

# Restart app
supervisorctl restart estate-vue

# Restart web server
systemctl reload nginx

# Check if app is running
curl http://127.0.0.1:5000/health
```

## 💰 **TOTAL COST**
- VPS: $3.99-7.99/month
- Domain: $8.99/year (optional)
- SSL: FREE
- **Total: ~$4-8/month**

## 🆘 **QUICK FIXES**
- **502 Error**: `supervisorctl restart estate-vue`
- **Domain not working**: Wait 24-48 hours for DNS
- **Permission errors**: `chown -R www-data:www-data /var/www/estate-vue`

---
✅ **Your Estate Vue website will be live with WhatsApp notifications working!**
