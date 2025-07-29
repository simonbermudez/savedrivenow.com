# SaveDriveNow - Auto Insurance Lead Management

A Django web application for managing auto insurance leads with a modern, responsive landing page similar to SaveDriveNow.com.

## Features

- **Modern Landing Page**: Clean, responsive design for lead capture
- **Lead Management**: Complete CRUD operations for insurance leads
- **Vehicle Information**: Track customer vehicle details (year, make, model)
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Docker Support**: Easy deployment with Docker containers

## Tech Stack

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (development) / PostgreSQL (production)
- **Deployment**: Docker, Nginx, Gunicorn

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Development Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd savedrivenow.com
```

2. Start the development environment:
```bash
./docker.sh dev
```
Or manually:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3. Access the application at `http://localhost:8000`

### Production Environment

1. Update environment variables in `docker-compose.prod.yml`
2. Start production environment:
```bash
./docker.sh prod
```

## Docker Commands

Use the included `docker.sh` script for easy container management:

```bash
./docker.sh dev           # Start development environment
./docker.sh prod          # Start production environment  
./docker.sh stop          # Stop all containers
./docker.sh build         # Build Docker image
./docker.sh logs          # Show container logs
./docker.sh shell         # Open shell in web container
./docker.sh migrate       # Run Django migrations
./docker.sh collectstatic # Collect static files
```

## Manual Setup (without Docker)

### Prerequisites
- Python 3.13+
- pip

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start development server:
```bash
python manage.py runserver
```

5. Access the application at `http://localhost:8000`

## Application Structure

```
savedrivenow.com/
├── docker-compose.yml          # Docker Compose configuration
├── docker-compose.dev.yml      # Development environment
├── docker-compose.prod.yml     # Production environment
├── Dockerfile                  # Docker image configuration
├── docker.sh                   # Docker management script
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database (development)
├── savedrivenow/               # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── leads/                      # Main application
    ├── models.py               # Lead data model
    ├── views.py                # Application views
    ├── forms.py                # Django forms
    ├── urls.py                 # URL routing
    └── templates/leads/        # HTML templates
        ├── landing.html        # Main landing page
        ├── lead_list.html      # Lead management
        ├── lead_detail.html    # Lead details
        └── lead_update.html    # Lead editing
```

## Features Details

### Landing Page
- Responsive hero section with gradient background
- Lead capture form with validation
- Vehicle information fields (optional)
- Modern UI with Bootstrap 5

### Lead Management
- Create, read, update, delete leads
- Search and pagination
- Vehicle information tracking
- Form validation and error handling

### Data Model
Each lead contains:
- Personal information (name, email, phone, birth date)
- Address information (street, city, state)
- Vehicle information (year, make, model)
- Timestamps (created, updated)

## Environment Variables

### Development
- `DEBUG=1`
- `SECRET_KEY=<your-secret-key>`
- `ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0`

### Production
- `DEBUG=0`
- `SECRET_KEY=<secure-secret-key>`
- `ALLOWED_HOSTS=<your-domain>`
- `POSTGRES_DB=savedrivenow`
- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=<secure-password>`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
