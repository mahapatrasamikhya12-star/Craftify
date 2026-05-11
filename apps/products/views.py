from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, SellerProfile
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter
from apps.users.permissions import IsSeller


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related(
        'seller', 'category').prefetch_related('images', 'reviews')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSeller()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # get the SellerProfile for this user — KEY FIX
        try:
            seller_profile = SellerProfile.objects.get(user=self.request.user)
        except SellerProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                "You need to become a seller first before adding products.")

        serializer.save(seller=seller_profile)  # pass SellerProfile not user

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.filter(is_active=True)
        return qs


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
