from django.urls import path
from .views import InitiatePaymentView, PaymentDetailView, PaymentListView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
