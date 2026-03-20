from rest_framework import serializers
from .models import Cart, CartItem



class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)   
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity', 'subtotal']
        
        
class CartSerializer(serializers.ModelSerializer):
            items = CartItemSerializer(many=True, read_only=True)
            total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
            
            
            class Meta:
                model = Cart
                fields = ['id', 'items', 'total', 'created_at']
                
                
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
                    
                    
                    
class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
                    
                    
                    
                    
