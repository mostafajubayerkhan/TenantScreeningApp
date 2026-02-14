# TenantScreeningApp - Getting Started Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Navigate to project directory**
   ```bash
   cd /Users/mostafakhan/Desktop/leasing_app/TenantScreeningApp
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Run the development server**
   ```bash
   ./venv/bin/python manage.py runserver
   ```

4. **Access the application**
   - Open your browser to: http://127.0.0.1:8000/

### Creating Your First Account

1. Click **"Get Started"** or **"Register"**
2. Choose your role: **Landlord** or **Tenant**
3. Fill in your details
4. Create a strong password
5. Click **"Create Account"**

### For Landlords

**Adding a Property:**
1. Log in and go to Dashboard
2. Click "Add New Property"
3. Fill in property details:
   - Title, Description
   - Address, City, State, ZIP
   - Bedrooms, Bathrooms, Square Feet
   - Monthly Rent, Security Deposit
   - Upload property image (optional)
4. Click "Create Property"

**Managing Applications:**
1. View applications from your Dashboard
2. Click "Review" on any application
3. View applicant details:
   - Personal information
   - Employment details
   - Income verification
4. Take action:
   - Mark Under Review
   - Approve
   - Reject

### For Tenants

**Browsing Properties:**
1. Click "Browse Properties" or "Browse" in the navigation
2. Use search/filter tools:
   - Search by keywords
   - Filter by city
   - Set minimum/maximum rent
3. Click "View Details" on any property

**Applying for a Property:**
1. View property details
2. Click "Apply for This Property"
3. Fill in the application:
   - Current address
   - Move-in date
   - Employment information
   - Income details
   - Number of occupants
   - Pet information (if applicable)
4. Click "Submit Application"
5. Track status from your Dashboard

### Admin Panel

Access Django admin at: http://127.0.0.1:8000/admin/

**Default Credentials** (if superuser was created):
- Username: admin
- Password: (set during superuser creation)

**Admin Features:**
- Manage all users
- Edit/delete properties
- Review all applications
- Access screening reports
- Manage leases

### File Structure

```
📁 TenantScreeningApp/
├── 📁 config/          # Django settings
├── 📁 core/            # Main application code
├── 📁 static/          # CSS, JS, images
├── 📁 templates/       # HTML templates
├── 📁 media/           # User uploads (created on first upload)
├── 📁 venv/            # Virtual environment
├── 📄 manage.py        # Django management script
└── 📄 requirements.txt # Python dependencies
```

### Common Commands

**Database Migrations** (if you modify models):
```bash
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
```

**Create Superuser**:
```bash
./venv/bin/python manage.py createsuperuser
```

**Collect Static Files** (for production):
```bash
./venv/bin/python manage.py collectstatic
```

### Troubleshooting

**Server won't start?**
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Static files not loading?**
- Ensure `DEBUG = True` in `config/settings.py`
- Check that `./venv/bin/python manage.py runserver` is running

**Can't log in?**
- Verify username and password
- Create a new account if needed
- Check that migrations have been applied

### Next Steps

1. **Create test data**: Add properties and submit applications to explore features
2. **Customize**: Edit templates and CSS to match your branding
3. **Extend**: Add new features like payments or notifications
4. **Deploy**: Set up for production with PostgreSQL and proper hosting

### Support

For detailed documentation, see:
- [Walkthrough](file:///Users/mostafakhan/.gemini/antigravity/brain/7bb3bc89-3cd8-4213-8faa-f5ced5d38a2e/walkthrough.md)
- [Implementation Plan](file:///Users/mostafakhan/.gemini/antigravity/brain/7bb3bc89-3cd8-4213-8faa-f5ced5d38a2e/implementation_plan.md)
