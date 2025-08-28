
# API views for Listing and Booking

import os
import requests
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """CRUD API for Listing"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger email task asynchronously
        send_mail.delay(booking.id, booking.customer.email)


# Load environment variables
load_dotenv(os.path.join(settings.BASE_DIR, '.env'))
CHAPA_SECRET_KEY = os.getenv('CHAPA_SECRET_KEY')
CHAPA_BASE_URL = os.getenv('CHAPA_BASE_URL', 'https://api.chapa.co/v1')


class PaymentInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        booking = get_object_or_404(Booking, id=booking_id)

        # Prepare Chapa payload
        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": request.user.email,
            "first_name": request.user.first_name or "User",
            "last_name": request.user.last_name or "",
            "tx_ref": str(booking.id),
            "callback_url": request.build_absolute_uri(f"/api/payments/verify/{booking.id}/"),
            "return_url": request.build_absolute_uri(f"/api/payments/verify/{booking.id}/"),
        }
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{CHAPA_BASE_URL}/transaction/initialize", json=payload, headers=headers)
        data = response.json()
        if response.status_code == 200 and data.get('status') == 'success':
            checkout_url = data['data']['checkout_url']
            transaction_id = data['data']['tx_ref']
            payment, created = Payment.objects.get_or_create(
                booking=booking,
                defaults={
                    'amount': amount,
                    'transaction_id': transaction_id,
                    'status': 'Pending',
                }
            )
            if not created:
                payment.transaction_id = transaction_id
                payment.amount = amount
                payment.status = 'Pending'
                payment.save()
            return Response({"checkout_url": checkout_url, "payment_id": str(payment.id)}, status=200)
        return Response({"error": data.get('message', 'Payment initiation failed')}, status=400)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        payment = get_object_or_404(Payment, booking__id=booking_id)
        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{CHAPA_BASE_URL}/transaction/verify/{payment.transaction_id}", headers=headers)
        data = response.json()
        if response.status_code == 200 and data.get('status') == 'success':
            payment.status = 'Completed'
            payment.save()
            # Send confirmation email (Celery task placeholder)
            from .tasks import send_payment_confirmation_email
            send_payment_confirmation_email.delay(request.user.email, booking_id)
            return Response({"status": "Completed"}, status=200)
        else:
            payment.status = 'Failed'
            payment.save()
            return Response({"status": "Failed", "detail": data.get('message', 'Verification failed')}, status=400)


# PaymentViewSet for admin or advanced usage
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
