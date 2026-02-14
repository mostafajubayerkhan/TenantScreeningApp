# Best Practices Guide - Reviewing & Running TenantScreeningApp

## 1. Code Review Checklist

### Django Settings Security Review
```bash
# Review settings.py for production readiness
cat config/settings.py
```

**Check these critical settings:**
- [ ] `DEBUG = False` for production (currently True for development)
- [ ] `SECRET_KEY` is not hardcoded (use environment variables)
- [ ] `ALLOWED_HOSTS` is properly configured
- [ ] Database credentials are in environment variables
- [ ] CSRF and security middleware are enabled

### Models Review
```bash
# Review all models for data integrity
./venv/bin/python manage.py check
```

**Verify:**
- [ ] All relationships have `on_delete` policies
- [ ] Unique constraints are in place where needed
- [ ] Field validators are appropriate
- [ ] String representations (`__str__`) are meaningful

### Views & Security Review
**Check for:**
- [ ] `@login_required` decorators on protected views
- [ ] Role-based permission checks (landlord vs tenant)
- [ ] CSRF tokens in all forms
- [ ] Input validation and sanitization
- [ ] No sensitive data in error messages

---

## 2. Testing the Application

### A. Manual Testing Flow

**Step 1: Test User Registration**
```bash
# Navigate to registration
open http://127.0.0.1:8000/register/
```
- [ ] Register as a **Landlord**
- [ ] Verify email validation works
- [ ] Test password strength requirements
- [ ] Confirm redirection to dashboard
- [ ] Logout and register as a **Tenant**

**Step 2: Test Landlord Workflow**
As landlord:
- [ ] Add a new property with all fields
- [ ] Upload a property image
- [ ] Edit existing property
- [ ] View property listing
- [ ] Check dashboard statistics

**Step 3: Test Tenant Workflow**
As tenant:
- [ ] Browse available properties
- [ ] Use search and filter features
- [ ] View property details
- [ ] Submit an application
- [ ] Verify cannot apply twice to same property
- [ ] Check dashboard for application status

**Step 4: Test Application Review**
As landlord:
- [ ] View pending applications
- [ ] Review application details
- [ ] Mark application as "Under Review"
- [ ] Approve an application
- [ ] Reject an application

**Step 5: Test Edge Cases**
- [ ] Try accessing landlord features as tenant (should fail)
- [ ] Try accessing tenant features as landlord (should fail)
- [ ] Submit empty forms (should show validation errors)
- [ ] Test with very long text inputs
- [ ] Test special characters in inputs

### B. Django Admin Testing
```bash
# Create superuser if not exists
./venv/bin/python manage.py createsuperuser

# Access admin panel
open http://127.0.0.1:8000/admin/
```

**Verify admin functionality:**
- [ ] All models are registered
- [ ] Search and filter work
- [ ] Inline editing works
- [ ] Can create/edit/delete records
- [ ] List display shows relevant fields

---

## 3. Database Review

### Check Database Integrity
```bash
# Verify all migrations are applied
./venv/bin/python manage.py showmigrations

# Check for any issues
./venv/bin/python manage.py check --database default
```

### Review Database Schema
```bash
# Access Django shell
./venv/bin/python manage.py shell
```

```python
# In Django shell, verify relationships
from core.models import User, Property, RentalApplication

# Check user counts by role
print(f"Landlords: {User.objects.filter(role='landlord').count()}")
print(f"Tenants: {User.objects.filter(role='tenant').count()}")

# Check property status distribution
from django.db.models import Count
print(Property.objects.values('status').annotate(count=Count('id')))

# Verify application constraints work
# (try creating duplicate application - should fail)
```

### Database Backup Best Practice
```bash
# Backup database (SQLite)
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# For production PostgreSQL, use:
# pg_dump dbname > backup.sql
```

---

## 4. Performance & Optimization Review

### Check for N+1 Query Problems
```bash
# Enable query debugging in Django shell
./venv/bin/python manage.py shell
```

```python
from django.db import connection
from django.test.utils import override_settings

# Test dashboard queries
from core.views import dashboard
# Monitor connection.queries for duplicate queries
```

**Optimization checklist:**
- [ ] Use `select_related()` for foreign keys
- [ ] Use `prefetch_related()` for reverse relations
- [ ] Add database indexes on frequently queried fields
- [ ] Implement pagination for long lists

### Static Files Check
```bash
# Verify static files are served correctly
ls -la static/css/
ls -la static/js/
ls -la static/images/

# In production, collect static files:
# ./venv/bin/python manage.py collectstatic
```

---

## 5. Security Audit

### A. Authentication & Authorization
- [ ] Passwords are hashed (Django default)
- [ ] Login attempts are protected
- [ ] Session management is secure
- [ ] Logout clears session properly
- [ ] Password reset flow exists (to be implemented)

### B. Input Validation
```bash
# Review forms.py for validation
cat core/forms.py
```
- [ ] All user inputs are validated
- [ ] File uploads have size limits
- [ ] File uploads restrict to images only
- [ ] XSS protection is in place

### C. Data Access Control
**Test scenarios:**
- [ ] Tenants cannot edit other users' applications
- [ ] Tenants cannot access landlord-only views
- [ ] Landlords can only see applications for their properties
- [ ] Users cannot view other users' profiles

---

## 6. Code Quality Review

### Check for Common Issues
```bash
# Run Django system checks
./venv/bin/python manage.py check --deploy

# Check for template syntax issues
find templates -name "*.html" -exec echo "Checking {}" \;
```

### Code Style & Standards
```bash
# Install code quality tools (optional)
pip install flake8 black

# Check code style
flake8 core/
black --check core/

# Format code
black core/
```

---

## 7. Browser Testing

### Cross-Browser Compatibility
Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Responsive Design Testing
Test at different viewport sizes:
- [ ] Desktop (1920px+)
- [ ] Tablet (768px - 1024px)
- [ ] Mobile (320px - 767px)

### UI/UX Review
- [ ] All buttons have hover states
- [ ] Forms show clear error messages
- [ ] Success messages are visible
- [ ] Navigation is intuitive
- [ ] Loading states are indicated

---

## 8. Documentation Review

### Essential Documentation
- [x] README.md exists
- [x] Walkthrough.md created
- [ ] API documentation (if applicable)
- [ ] Deployment guide
- [ ] Environment setup guide

### Code Comments
- [ ] Complex logic is commented
- [ ] Model fields have help_text
- [ ] View docstrings explain purpose
- [ ] Form validation rules are documented

---

## 9. Pre-Production Checklist

### Before Deploying to Production

**Environment Configuration:**
```bash
# Create .env file for environment variables
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EOF
```

**Security Settings:**
- [ ] Install `django-environ` for environment variables
- [ ] Generate new SECRET_KEY
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure SECURE_* settings
- [ ] Set up CORS if needed

**Database:**
- [ ] Migrate to PostgreSQL (from SQLite)
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Optimize database indexes

**Static & Media Files:**
- [ ] Configure S3/CDN for media files
- [ ] Run `collectstatic`
- [ ] Set up proper media file permissions
- [ ] Configure file upload size limits

**Monitoring & Logging:**
- [ ] Set up error logging (Sentry/Rollbar)
- [ ] Configure Django logging
- [ ] Set up performance monitoring
- [ ] Enable database query logging

---

## 10. Quick Testing Script

Save this as `test_app.sh`:

```bash
#!/bin/bash

echo "🧪 Starting TenantScreeningApp Testing..."

# Activate virtual environment
source venv/bin/activate

# Run Django checks
echo "\n📋 Running Django system checks..."
./venv/bin/python manage.py check

# Check migrations
echo "\n🗄️  Checking migrations..."
./venv/bin/python manage.py showmigrations

# Run test server
echo "\n🚀 Starting development server..."
./venv/bin/python manage.py runserver
```

Make executable:
```bash
chmod +x test_app.sh
./test_app.sh
```

---

## Summary: Your Testing Workflow

### Daily Development Testing:
1. ✅ Run `python manage.py check`
2. ✅ Test new features manually in browser
3. ✅ Check for console errors (browser DevTools)
4. ✅ Verify data saves correctly in admin panel

### Before Each Commit:
1. ✅ Review code changes
2. ✅ Test affected functionality
3. ✅ Check for breaking changes
4. ✅ Update documentation if needed

### Before Production Deployment:
1. ✅ Complete full security audit
2. ✅ Run all tests (when implemented)
3. ✅ Performance testing
4. ✅ Database backup
5. ✅ Review error logging setup

---

## Next Steps

1. **Implement Unit Tests**: Create `core/tests.py` with test cases
2. **Set Up CI/CD**: Automate testing and deployment
3. **Add Integration Tests**: Test complete user workflows
4. **Performance Testing**: Use tools like Locust or Apache JMeter
5. **Security Scanning**: Use tools like Bandit for Python security
