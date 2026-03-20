from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_name', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        
    def validate(self, data):
        request = self.context.get('request')
        product = data.get('product')
        if request and request.method == 'POST':
            if Review.objects.filter(user=request.user, product=product).exists():
                raise serializers.ValidationError("You have already reviewed this product.") 
        return data   