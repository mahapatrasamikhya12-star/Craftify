from django.db import models
from django.conf import settings


class Category(models.Model):
    name   = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True,
                on_delete=models.SET_NULL, related_name='subcategories')
    icon   = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE, related_name='seller')
    shop_name   = models.CharField(max_length=100, unique=True)
    bio         = models.TextField(blank=True)
    banner      = models.ImageField(upload_to='banners/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name


class Product(models.Model):
    seller       = models.ForeignKey(SellerProfile, on_delete=models.CASCADE,
                       related_name='products')
    category     = models.ForeignKey(Category, on_delete=models.SET_NULL,
                       null=True, blank=True, related_name='products')
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    discount_pct = models.FloatField(default=0)
    stock_qty    = models.IntegerField(default=0)
    is_handmade  = models.BooleanField(default=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE,
                    related_name='images')
    image      = models.ImageField(upload_to='products/')
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                related_name='tags')
    tag     = models.CharField(max_length=50)

    class Meta:
        unique_together = ('product', 'tag')

    def __str__(self):
        return self.tag