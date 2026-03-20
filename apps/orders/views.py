from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status  # ✅ added missing imports
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer, PlaceOrderSerializer
from apps.products.models import Product


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = Order.objects.create(
            buyer=request.user,
            shipping_address=data['shipping_address']
        )

        for item_data in data['items']:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                continue

            quantity = item_data.get('quantity', 1)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            # ✅ Fixed: model uses stock_qty not stock
            product.stock_qty -= quantity
            product.save()

        order.calculate_total()
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            buyer=self.request.user
        ).prefetch_related('items__product').order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ fixed capital P

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, buyer=request.user)
        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Order cannot be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save()
        # Restore stock
        for item in order.items.all():
            if item.product:
                item.product.stock_qty += item.quantity  # ✅ fixed
                item.product.save()
        return Response({'message': 'Order cancelled successfully.'})