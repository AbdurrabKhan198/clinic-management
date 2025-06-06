# Production Setup Guide - PostgreSQL

This guide will help you deploy your clinic management system with PostgreSQL in production.

## Prerequisites

1. PostgreSQL server installed and running
2. Python environment with all dependencies installed
3. Web server (nginx/apache) configured
4. SSL certificate (recommended)

## Step 1: Install Dependencies

```bash
# Install the updated requirements
pip install -r requirements.txt
```

## Step 2: PostgreSQL Setup

### Install PostgreSQL (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE clinic_management;

# Create user
CREATE USER clinic_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE clinic_management TO clinic_user;

# Exit psql
\q
```

## Step 3: Environment Configuration

### Option A: Using Environment Variables

Set these environment variables in your production environment:

```bash
export SECRET_KEY="your-super-secret-key-here-change-this-in-production"
export DEBUG="False"
export DB_NAME="clinic_management"
export DB_USER="clinic_user"
export DB_PASSWORD="your_secure_password"
export DB_HOST="localhost"
export DB_PORT="5432"
```

### Option B: Using .env file (with python-decouple)

1. Install python-decouple: `pip install python-decouple`
2. Copy `production.env.example` to `.env`
3. Update the values in `.env` file
4. Update settings.py to use decouple (see below)

## Step 4: Django Database Migration

```bash
# Run migrations to create tables in PostgreSQL
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 5: Test the Setup

```bash
# Test database connection
python manage.py dbshell

# Run the development server to test
python manage.py runserver
```

## Step 6: Production Deployment

### Using Gunicorn (recommended)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn crm.wsgi:application --bind 0.0.0.0:8000
```

### Using systemd service

Create `/etc/systemd/system/clinic-management.service`:

```ini
[Unit]
Description=Clinic Management Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/clinic-management
Environment="SECRET_KEY=your-secret-key"
Environment="DEBUG=False"
Environment="DB_NAME=clinic_management"
Environment="DB_USER=clinic_user"
Environment="DB_PASSWORD=your_password"
Environment="DB_HOST=localhost"
Environment="DB_PORT=5432"
ExecStart=/path/to/clinic-management/clinic_env/bin/gunicorn crm.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## Step 7: Nginx Configuration

Create `/etc/nginx/sites-available/clinic-management`:

```nginx
server {
    listen 80;
    server_name zospital.in www.zospital.in;

    location /static/ {
        alias /path/to/clinic-management/staticfiles/;
    }

    location /media/ {
        alias /path/to/clinic-management/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Step 8: SSL Configuration (Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d zospital.in -d www.zospital.in
```

## Step 9: Database Backup Strategy

### Daily Backup Script

Create `/home/backup/backup_db.sh`:

```bash
#!/bin/bash
DATE=$(date +"%Y%m%d_%H%M%S")
pg_dump -h localhost -U clinic_user -d clinic_management > /home/backup/clinic_backup_$DATE.sql
find /home/backup -name "clinic_backup_*.sql" -mtime +7 -delete
```

Add to crontab:

```bash
0 2 * * * /home/backup/backup_db.sh
```

## Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Set DEBUG=False in production
- [ ] Configured ALLOWED_HOSTS properly
- [ ] Database user has minimal required permissions
- [ ] SSL/HTTPS configured
- [ ] Regular database backups scheduled
- [ ] Firewall configured to limit database access
- [ ] Server and dependencies kept updated

## Troubleshooting

### Common Issues

1. **Connection refused error**

   - Check if PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify database credentials

2. **Permission denied**

   - Check database user permissions
   - Verify file permissions for Django application

3. **Static files not loading**

   - Run `python manage.py collectstatic --noinput`
   - Check nginx static file configuration

4. **Migration errors**
   - Ensure database is empty before first migration
   - Check for any custom migration dependencies

### Logs

- Django logs: Check your application logs
- PostgreSQL logs: `/var/log/postgresql/`
- Nginx logs: `/var/log/nginx/`

## Performance Optimization

1. **Database Indexing**: Review and add indexes for frequently queried fields
2. **Connection Pooling**: Consider using pgbouncer for connection pooling
3. **Caching**: Implement Redis/Memcached for caching
4. **Static Files**: Use CDN for static files in high-traffic scenarios

---

**Important**: Always test your production setup in a staging environment first!
