# Movement Credit A.I. - Credit Repair Automation System

## Deployment Instructions

1. **Create a new Render.com account** (if you don't have one)
2. **Create a new Web Service** in your Render dashboard
3. **Connect your GitHub repository** containing this code
4. **Set environment variables** in Render dashboard:
   - `SECRET_KEY`: Your Flask secret key
   - `DATABASE_URL`: PostgreSQL connection string
   - `EMAIL_USER`: Your email username
   - `EMAIL_PASS`: Your email password
   - `STRIPE_SECRET_KEY`: Your Stripe secret key
   - `STRIPE_PUBLIC_KEY`: Your Stripe publishable key
5. **Deploy** the application

## System Features

- High-conversion landing page with urgency elements
- Automated dispute letter generation
- Credit repair CRM with client management
- Secure document handling
- Payment processing via Stripe
- Email notifications

## Technical Stack

- Python 3.9
- Flask
- PostgreSQL
- SQLAlchemy
- Stripe API
- Gunicorn