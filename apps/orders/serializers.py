from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.title', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name',
                  'product_image', 'quantity', 'price', 'subtotal']

    def get_product_image(self, obj):
        if obj.product:
            images = obj.product.images.filter(is_primary=True).first()
            if images:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(images.image.url)
                return images.image.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price',
                  'shipping_address', 'created_at', 'items']


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity   = serializers.IntegerField(default=1)


class PlaceOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    items = OrderItemInputSerializer(many=True)