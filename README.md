# Hotel Room Booking API

This is a REST API for managing hotel room bookings. It is built with Django and Django REST Framework.

## Tech Stack
- Python 3.12+
- Django 6.0
- Django REST Framework
- PostgreSQL
- drf-spectacular (Swagger)
- Ruff (Linter and Formatter)

## How to Run the Application

### 1. Setup Environment
```bash
# Clone the project
git clone <repository_url>
cd room_booking

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Database and Migrations
Ensure PostgreSQL is running and you have a database named room_booking. If you use different settings, update room_booking/settings.py.

```bash
cd room_booking
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Start Server
```bash
python manage.py runserver
```
The application will be available at http://127.0.0.1:8000/

## API Documentation

- Swagger UI: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/

### API Usage Flow:
1. Register a new user at POST /api/register/.
2. Login at POST /api/login/ to receive a token.
3. Use the token in the Authorization header: Token <your_token>.
4. In Swagger, click Authorize and enter: Token <your_token>.

## Code Quality
To check code style or format the code, use Ruff:

```bash
# Check for errors
ruff check .

# Format code
ruff format .
```
