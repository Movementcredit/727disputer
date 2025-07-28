# 727disputer (Movement Credit A.I.)

## Overview
Movement Credit A.I. automates credit repair dispute letters, CRM, secure document handling, Stripe payments, and email notifications. Dual-mode for agencies and consumers. Fully compliant, notarization-ready.

## Features
- Automated FCRA/FDCPA/Metro 2 dispute letter generation
- CRM for client management
- Secure document handling
- Stripe payment integration
- Email notifications
- High-conversion landing page
- Agency/consumer dual-mode


## Deployment

### Option 1: Render.com
1. Create a Render.com account
2. Create a new Web Service
3. Connect your GitHub repo
4. Ensure the following files are in your repo root:
   - `Procfile` with: `web: gunicorn "app:create_app()"`
   - `runtime.txt` with: `python-3.9.7`
5. Set environment variables:
   - SECRET_KEY
   - DATABASE_URL
   - EMAIL_USER
   - EMAIL_PASS
   - STRIPE_SECRET_KEY
   - STRIPE_PUBLIC_KEY
6. In Render, use "Manual Deploy" > "Clear build cache & deploy" to ensure the correct Python version and Procfile are used.
7. Deploy

### Option 2: Azure App Service
1. Create an Azure account and install the Azure CLI (`az`)
2. Login: `az login`
3. Create a resource group: `az group create --name flask-rg --location eastus`
4. Create an App Service plan: `az appservice plan create --name flask-plan --resource-group flask-rg --sku FREE`
5. Create a Web App: `az webapp create --resource-group flask-rg --plan flask-plan --name <your-unique-app-name> --runtime "PYTHON|3.9"`
6. Set environment variables:
   `az webapp config appsettings set --resource-group flask-rg --name <your-unique-app-name> --settings SECRET_KEY=... DATABASE_URL=... EMAIL_USER=... EMAIL_PASS=... STRIPE_SECRET_KEY=... STRIPE_PUBLIC_KEY=...`
7. Deploy your code via local git or GitHub Actions
8. Set the startup command:
   `az webapp config set --resource-group flask-rg --name <your-unique-app-name> --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 'app:create_app()'"`
9. Browse to your app: `az webapp browse --resource-group flask-rg --name <your-unique-app-name>`

## Compliance & Notarization
- All dispute letters include notarization blocks, certified mail envelope formatting, and compliance metadata.
- Print-ready layouts for legal and audit use.

## Tech Stack
- Python 3.9
- Flask
- PostgreSQL
- SQLAlchemy
- Stripe
- Gunicorn

## Contact
movementcredit251@gmail.com
