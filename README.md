# School Management System

A comprehensive web-based portal for managing school operations, including student registration, admission processes, and administrative tasks. Built with Django framework and featuring robust user authentication for school employees.

## Features

- Student registration and admission management
- Employee authentication system (Django's built-in authentication)
- Administrative dashboard
- Database management through Django admin interface
- RESTful API endpoints for data exchange

## Prerequisites

- Python 3.x
- Django
- pip (Python package installer)

## Installation & Setup

### 1. Clean Migration Files
Before starting, clean up any existing migration and cache files:
```bash
# Delete all migration files except __init__.py
# Delete all __pycache__ directories
# Keep only the __init__.py files in migration folders
```

### 2. Install Dependencies
Install all required packages from the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Create Django Project (If Starting Fresh)
```bash
# Create new Django project
python -m django startproject project_name

# Navigate to project directory
cd project_name

# Create Django app
python -m django startapp app_name
```

## Project Structure

### Root Directory
- `manage.py` - Django's command-line utility for administrative tasks
- `project_name/` - Main project directory
- `app_name/` - Application directory

### Key Files

#### Project Directory (`project_name/`)
- **`urls.py`** - Main URL configuration for routing
- **`settings.py`** - Project settings including:
  - Static files configuration (CSS, JS)
  - Templates directory
  - Database configuration
  - Media files for images and videos

#### App Directory (`app_name/`)
- **`views.py`** - Contains application logic and request handling
- **`models.py`** - Database models and table definitions
- **`admin.py`** - Admin interface configuration
- **`urls.py`** - App-specific URL patterns
- **`serializers.py`** - API serializers for data formatting

## Database Setup

### Apply Migrations
```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Check Migration Status
```bash
# View migration history
python manage.py showmigrations
```

**Note:** This project includes existing migration history. If you encounter migration errors, manually review and clean the migration files before proceeding.

## Running the Application

1. Ensure all URLs are properly configured
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and navigate to: `http://127.0.0.1:8000`

## Admin Interface

### Create Superuser
Before accessing the admin panel, you need to create a superuser account:
```bash
python manage.py createsuperuser
```
You will be prompted to enter:
- **Username** - Your admin username
- **Email** - Your email address (optional)
- **Password** - Secure password (entered twice for confirmation)

### Access Admin Panel
After creating the superuser, access the Django admin panel at `http://127.0.0.1:8000/admin` to:
- Manage database records
- Add or remove data without direct database access
- Monitor registered models
- Manage user accounts and permissions

## API Endpoints

The application includes RESTful API endpoints that use serializers to format data for external consumption.

## Troubleshooting

### Migration Issues
- Check migration history: `python manage.py showmigrations`
- Manually remove problematic migration files
- Clear database and start fresh if necessary

### General Issues
This is a learning project. If you encounter persistent issues:
1. Create a fresh Django project and app
2. Copy the application code to your new project
3. Ensure clean migration history

## Important Notes

- This is an educational project designed for learning Django concepts
- Database migration loops may occur if migration history isn't properly cleared
- Always backup your data before making structural changes

## Contributing

This project is intended for educational purposes. Feel free to fork, modify, and use the code for your own learning projects.

## License

This project is for educational use only.
