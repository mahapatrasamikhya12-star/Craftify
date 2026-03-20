from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['id', 'order', 'amount', 'status']
    list_filter   = ['status']
    search_fields = ['gateway_ref']