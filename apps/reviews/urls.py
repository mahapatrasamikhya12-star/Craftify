from django.urls import path
from .views import ProductReviewListView, ReviewDetailView

urlpatterns = [
    path('product/<int:product_id>/', ProductReviewListView.as_view(), name='product-reviews'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail',)
]
