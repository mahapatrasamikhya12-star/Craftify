import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer, InitiatePaymentSerializer
from apps.orders.models import Order

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = get_object_or_404(Order, id=serializer.validated_data['order_id'], buyer=request.user)
        
        if hasattr(order,'payment') and order.payment.status == 'paid':
            return Response({'error': 'Order is already paid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'amount': order.total,
                'method': serializer.validated_data['method'],
                'status': 'pending',
            }
        )
        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )
class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        payment = get_object_or_404(
            Payment,
            pk=pk,
            order__buyer=request.user
        )
        return Response(PaymentSerializer(payment).data)


class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(
            order__buyer=request.user
        ).order_by('-id')
        return Response(PaymentSerializer(payments, many=True).data)