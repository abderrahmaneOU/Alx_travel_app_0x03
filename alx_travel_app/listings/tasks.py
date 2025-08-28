from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(email, booking_id):
    subject = "Payment Successful"
    message = f"Your payment for booking {booking_id} was successful."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )

@shared_task
def send_booking_email(booking_id, customer_email):
    subject = "Booking Confirmation"
    message = f"Your booking with ID {booking_id} has been confirmed!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [customer_email]
    send_mail(subject, message, from_email, recipient_list)
