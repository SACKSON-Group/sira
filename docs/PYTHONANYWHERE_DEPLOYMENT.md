# PythonAnywhere Deployment Guide for SIRA

This guide walks you through deploying the SIRA platform to PythonAnywhere.

## Prerequisites

- PythonAnywhere account (Hacker plan or above recommended for custom domains)
- GitHub repository with SIRA code pushed

## Step 1: Create PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com)
2. Sign up for an account (Hacker plan recommended)
3. Verify your email

## Step 2: Clone Repository

1. Open a **Bash console** from the Dashboard
2. Clone your repository:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/sira.git
cd sira
```

## Step 3: Set Up Virtual Environment

```bash
# Create virtual environment with Python 3.11
mkvirtualenv --python=/usr/bin/python3.11 sira

# Activate it (if not already active)
workon sira

# Install backend dependencies
cd ~/sira/backend
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Create the `.env` file:

```bash
cd ~/sira/backend
cp .env.example .env
nano .env
```

2. Update the following values:

```env
# Database - Use MySQL on PythonAnywhere
DATABASE_URL=mysql+pymysql://YOUR_USERNAME$sira:YOUR_DB_PASSWORD@YOUR_USERNAME.mysql.pythonanywhere-services.com/YOUR_USERNAME$sira

# Security - Generate new keys!
SECRET_KEY=your-super-secret-key-generate-with-openssl-rand-hex-32
JWT_SECRET_KEY=your-jwt-secret-key-generate-with-openssl-rand-hex-32

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=production
DEBUG=false
```

Generate secure keys:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 5: Set Up MySQL Database

1. Go to **Databases** tab on PythonAnywhere Dashboard
2. Set a MySQL password
3. Create a database named `YOUR_USERNAME$sira`
4. Note down the database host: `YOUR_USERNAME.mysql.pythonanywhere-services.com`

## Step 6: Initialize Database

```bash
workon sira
cd ~/sira/backend

# Run migrations
alembic upgrade head

# Create admin user
python create_admin.py
```

## Step 7: Configure Web App

1. Go to **Web** tab on PythonAnywhere Dashboard
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Choose **Python 3.11**

### Configure Virtual Environment

In the **Virtualenv** section:
```
/home/YOUR_USERNAME/.virtualenvs/sira
```

### Configure WSGI File

1. Click on the WSGI configuration file link
2. Delete all contents and replace with:

```python
import sys
import os

# Add your project to the path
project_home = '/home/YOUR_USERNAME/sira/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['DATABASE_URL'] = 'mysql+pymysql://YOUR_USERNAME$sira:PASSWORD@YOUR_USERNAME.mysql.pythonanywhere-services.com/YOUR_USERNAME$sira'
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['JWT_SECRET_KEY'] = 'your-jwt-secret'
os.environ['ENVIRONMENT'] = 'production'

# Import and run the FastAPI app
from app.main import app
application = app
```

## Step 8: Configure Static Files (Frontend)

### Build Frontend Locally

On your local machine:
```bash
cd frontend
npm install
npm run build
```

### Upload to PythonAnywhere

1. Upload the `dist` folder contents to `/home/YOUR_USERNAME/sira/frontend/dist`
2. In the **Web** tab, add a static file mapping:

| URL | Directory |
|-----|-----------|
| /static | /home/YOUR_USERNAME/sira/frontend/dist |
| /assets | /home/YOUR_USERNAME/sira/frontend/dist/assets |

## Step 9: Configure CORS

Update `backend/app/main.py` with your PythonAnywhere domain:

```python
origins = [
    "https://YOUR_USERNAME.pythonanywhere.com",
    "http://YOUR_USERNAME.pythonanywhere.com",
]
```

## Step 10: Reload Web App

1. Go to **Web** tab
2. Click **Reload** button

## Step 11: Verify Deployment

1. Visit `https://YOUR_USERNAME.pythonanywhere.com/health`
2. You should see: `{"status": "healthy", "version": "1.0.0"}`

## Step 12: Access the Application

- API Docs: `https://YOUR_USERNAME.pythonanywhere.com/docs`
- Frontend: `https://YOUR_USERNAME.pythonanywhere.com`

## Troubleshooting

### View Error Logs

```bash
# In PythonAnywhere console
cat /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Common Issues

1. **ModuleNotFoundError**: Ensure virtualenv is correctly configured
2. **Database connection errors**: Verify MySQL credentials and host
3. **Static files not loading**: Check static file mappings

### Updating the Application

```bash
cd ~/sira
git pull origin main
workon sira
cd backend
pip install -r requirements.txt
alembic upgrade head
```

Then reload the web app from the Dashboard.

## Custom Domain (Optional)

1. Go to **Web** tab
2. Add your custom domain
3. Configure DNS CNAME record pointing to `webapp-XXXXXX.pythonanywhere.com`

## Scheduled Tasks

For background tasks (optional):

1. Go to **Tasks** tab
2. Add daily task:
```bash
workon sira && cd ~/sira/backend && python -c "from app.services.alert_engine import AlertEngine; AlertEngine().process_pending_events()"
```

## Security Checklist

- [ ] Changed default SECRET_KEY
- [ ] Changed default JWT_SECRET_KEY
- [ ] Set DEBUG=false
- [ ] Configured HTTPS
- [ ] Set strong database password
- [ ] Created unique admin password
