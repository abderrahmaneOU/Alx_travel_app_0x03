
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, PaymentViewSet, PaymentInitiateView, PaymentVerifyView


router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/payments/initiate/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('api/payments/verify/<uuid:booking_id>/', PaymentVerifyView.as_view(), name='payment-verify'),
]
