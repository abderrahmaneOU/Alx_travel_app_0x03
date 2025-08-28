# ALX Travel App

- Book listings for specific dates

pip install -r requirements.txt

- Bookings: `/api/bookings/`

- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

````markdown
# ALX Travel App

This is the Django project for ALX Travel App.

## Features

- Create and manage travel listings
- Book listings for specific dates
- Leave reviews and ratings
- REST API-ready (Django REST Framework)
- Chapa payment integration for bookings
- Payment confirmation emails (Celery)
- API documentation with Swagger (drf-yasg)

## Setup Instructions

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the `alx_travel_app` directory with:

```
CHAPA_SECRET_KEY=your_chapa_secret_key_here
CHAPA_BASE_URL=https://api.chapa.co/v1
```

## API Endpoints

- Listings: `/api/listings/`
- Bookings: `/api/bookings/`
- Payments: `/api/payments/` (CRUD)
- Initiate Payment: `/api/payments/initiate/` (POST)
- Verify Payment: `/api/payments/verify/<booking_id>/` (GET)

Supports: GET, POST, PUT, DELETE for main endpoints.

### Payment Workflow

1. User books a listing (POST to `/api/bookings/`).
2. Initiate payment (POST to `/api/payments/initiate/` with `booking_id` and `amount`).
3. User is redirected to Chapa checkout.
4. After payment, verify status (GET `/api/payments/verify/<booking_id>/`).
5. On success, user receives confirmation email.

## API Documentation

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

You can use Swagger UI to test all endpoints interactively.

## Testing Chapa Integration

- Use Chapa sandbox credentials for testing.
- Check logs for payment initiation, verification, and status updates.

## Celery

- Celery is used for sending confirmation emails asynchronously.
````
