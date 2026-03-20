from rest_framework import serializers
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'sort_order']


class ProductSerializer(serializers.ModelSerializer):
    images       = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name  = serializers.CharField(source='seller.shop_name', read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price',
            'discount_pct', 'stock_qty', 'is_handmade', 'is_active',
            'category', 'category_name',
            'seller', 'seller_name',
            'images', 'uploaded_images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'seller', 'created_at', 'updated_at']

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for i, image in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(i == 0),
                sort_order=i
            )
        return product