# AITrip Backend Server Documentation

## Project Overview

AITrip is a backend API service built with Django REST Framework that provides travel-related functionalities.

## System Requirements

- Python 3.10 or higher
- It is recommended to use Anaconda to install Python and manage packages

## Quick Start

### 1. Project Structure

```
AITrip/
├── AITrip/                 # Django project configuration directory
│   ├── __init__.py
│   ├── settings.py         # Project configuration (database settings here)
│   ├── urls.py             # URL routing configuration
│   ├── wsgi.py
│   └── asgi.py
├── manage.py               # Django management script
├── requirements.txt        # Project dependency list
├── start_server.py         # One-click start script
└── README.md               # Documentation
```

### 2. One-Click Start (Recommended)

The easiest way to start is by using the provided script:

```
python start_server.py
```

This script will automatically:

1. Check and install all dependencies
2. Run database migrations
3. Create a superuser account
4. Start the development server

### 3. Manual Start Steps

If you want more control, you can follow these steps manually:

#### Step 1: Install dependencies

```
pip install -r requirements.txt
```

#### Step 2: Run database migrations

```
python manage.py makemigrations
python manage.py migrate
```

#### Step 3: Create superuser (optional)

```
python manage.py createsuperuser
```

#### Step 4: Start server

```
python manage.py runserver 8080
```

## Database Configuration

### MySQL Database Setup

The project uses MySQL as the database. Follow these steps:

#### 1. Install MySQL driver

```
pip install mysqlclient
```

#### 2. Create MySQL database

Manually create a database in MySQL.

#### 3. Add `DB_PASSWORD` to system environment variables

- Variable name: `DB_PASSWORD`
- Value: your database password

#### 4. Update `AITrip/settings.py`

Locate the `DATABASES` section (around line 75) and replace with:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aitrip_db',           # Database name
        'USER': 'aitrip_user',         # Database user
        'PASSWORD': 'aitrip123',       # Database password
        'HOST': 'localhost',           # Database host
        'PORT': '3306',                # Database port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## Access Points

Once the server is running, you can access:

- **Backend API Service**: http://localhost:8080
- **Django Admin Panel**: http://localhost:8080/admin
- **API Documentation**: http://localhost:8080/api/

## Default Superuser Account

When using the one-click script, the following superuser will be created:

- **Username**: admin
- **Email**: admin@aitrip.com
- **Password**: admin123

## Common Issues

### 1. Port already in use

If port 8080 is in use, specify another port:

```
python manage.py runserver 8081
```

### 2. Dependency installation failed

Make sure you’re using Python 3.10+:

```
python --version
pip --version
```

### 3. Database connection failed

Check if the database service is running, username/password are correct, and the database exists.

## Project Dependencies

The main dependencies include:

```
Django==5.2                     # Django core framework
djangorestframework==3.16.0     # REST API framework
django-cors-headers==4.7.0      # CORS handling
django-filter==25.1             # API filtering
djangorestframework-simplejwt==5.5.0  # JWT authentication
```

## Development Recommendations

1. **Use virtual environments**: Prevent package conflicts
2. **Version control**: Do not commit sensitive information (like DB passwords)
3. **Code style**: Use `black` and `flake8` for formatting and linting
4. **Testing**: Write tests to ensure code quality

## Support

If you encounter problems, check:

1. Python version
2. Dependencies installed correctly
3. Database configuration
4. Port availability

---

