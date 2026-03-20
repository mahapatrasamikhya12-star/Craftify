from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from apps.products.models import Product

class ProductReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_permission(self):
        if self.request.method == 'POST':
            return [permission.IsAuthenticated()]
        return [permission.AllowAny()] 
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(Product_id=Product_id).select_related('user')
    
    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        serializer.save(user=self.request.user, product=product)
        
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)          