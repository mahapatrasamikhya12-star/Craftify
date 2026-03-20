from django.contrib import admin
from .models import Category, Product, ProductImage, ProductTag, SellerProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name']
    search_fields = ['name']


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display  = ['id', 'shop_name', 'is_verified']
    list_filter   = ['is_verified']
    search_fields = ['shop_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'seller', 'price']
    search_fields = ['title']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'is_primary']


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'tag']