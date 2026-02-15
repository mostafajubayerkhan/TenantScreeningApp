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

### Premium Landlord Features

- **Landlord Analytics Dashboard**: Interactive charts tracking property views and applicant quality (Trust Scores) using `Chart.js`.
- **Verified Screening APIs (Mocked)**: Process comprehensive credit and background checks for $30, generating a premium report.
- **AI-Powered Lease Generator**: Create professional, 13-clause residential lease agreements instantly.
- **Tenant Trust Scores**: A badge-based system (Gold, Silver, Bronze) to help landlords identify top-tier applicants at a glance.

### Modern Design & Aesthetics

- **Glassmorphism UI**: Frosted-glass effects on headers, search bars, and navigation.
- **Dynamic Animations**: Smooth hover transforms, fade-in-up hero sections, and glow effects on primary calls-to-action.
- **Responsive Charts**: Data-driven insights visualized through interactive line and doughnut charts.

### File Structure

```
📁 TenantScreeningApp/
├── 📁 config/          # Django settings
├── 📁 core/            # Main application logic (Models, Views, Forms)
├── 📁 static/          # CSS Design System & Chart.js integration
├── 📁 templates/       # Premium HTML templates with Glassmorphism
├── 📁 media/           # User uploads (Properties, Profiles)
├── 📁 venv/            # Virtual environment
├── 📄 manage.py        # Django management script
└── 📄 requirements.txt # Python dependencies
```

### Common Commands

**Database Migrations**:
```bash
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
```

**Run Development Server**:
```bash
./venv/bin/python manage.py runserver
```

**Create Superuser**:
```bash
./venv/bin/python manage.py createsuperuser
```

### Next Steps

1. **Deploy to Production**: Ready for Heroku/AWS with minor config tweaks.
2. **Stripe Integration**: Connect real payments for screening fees.
3. **Live API Connection**: Swap mock services for actual Checkr or TransUnion APIs.

### Support

For detailed developers guide and proof of work, see:
- [Walkthrough](/Users/mostafakhan/.gemini/antigravity/brain/7bb3bc89-3cd8-4213-8faa-f5ced5d38a2e/walkthrough.md)
- [Implementation Plan](/Users/mostafakhan/.gemini/antigravity/brain/7bb3bc89-3cd8-4213-8faa-f5ced5d38a2e/implementation_plan.md)
- [Task Progress](/Users/mostafakhan/.gemini/antigravity/brain/7bb3bc89-3cd8-4213-8faa-f5ced5d38a2e/task.md)
