# Django Project Setup Guide

This Django project can be run either locally using Django's development server or with Docker. Below are instructions for both methods.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Docker and Docker Compose (for Docker setup)
- Virtual environment tool (recommended)

## Local Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Docker Setup

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at http://localhost:8000/

### Docker Commands Reference

- Start containers in detached mode:
  ```bash
  docker-compose up -d
  ```

- Stop containers:
  ```bash
  docker-compose down
  ```

- View logs:
  ```bash
  docker-compose logs -f
  ```

- Execute commands in the container:
  ```bash
  docker-compose exec web [command]
  ```

## Project Structure

```
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Key Files

- `requirements.txt`: Python dependencies
- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker container configuration
- `.env`: Environment variables (not tracked in git)
- `.env.example`: Example environment variables template

## Development Guidelines

1. Always work in the virtual environment when developing locally
2. Add new dependencies to `requirements.txt`
3. Run tests before committing:
   ```bash
   python manage.py test
   ```

## Common Issues and Solutions

1. Database connection errors:
   - Check if PostgreSQL service is running (for local setup)
   - Verify database credentials in .env file
   - Ensure migrations are applied

2. Port conflicts:
   - Change the port in docker-compose.yml if 8000 is already in use
   - For local development: `python manage.py runserver 8001`

## Deployment

Instructions for deploying to production environments will vary based on your hosting solution. Common options include:

- Heroku
- DigitalOcean
- AWS
- Google Cloud Platform

Refer to the specific platform's documentation for detailed deployment instructions.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
