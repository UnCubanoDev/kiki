from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import path

from .models import (Restaurant, Category, Distributor, DistributorRating,
                     OrderDetail, ProductRating, Product, Order, RestaurantRating, Configuration, ProductCategory, Metrics)

from solo.admin import SingletonModelAdmin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone
from datetime import timedelta
from .admin_views import DashboardView


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user',
        'phone',
        'is_active',
        'funds',
        'display_business_type',
    ]
    list_filter = ['is_active']
    search_fields = ['name', 'user__username', 'phone']

    def display_business_type(self, obj):
        return ", ".join([category.name for category in obj.business_type.all()])
    display_business_type.short_description = 'Business Type'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    list_display = ['user', 'vehicle_id',
                    'vehicle_type', 'rating', 'total_gain', 'debt']
    pass


@admin.register(DistributorRating)
class DistributorRatingAdmin(admin.ModelAdmin):
    pass


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0
    readonly_fields = ['product', 'quantity', 'get_final_price', 'restaurant']
    fields = ['product', 'quantity', 'get_final_price', 'restaurant']

    def get_final_price(self, obj):
        return obj.get_final_price()  # Asegúrate de que este método exista en OrderDetail

    def save_related(self, request, form, change):
        super().save_related(request, form, change)
        for order_detail in form.instance.products.all():
            if not order_detail.unit_price:  # Solo si el precio no está establecido
                order_detail.unit_price = order_detail.product.price
                order_detail.save()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'status',
        'note',
    ]
    inlines = [OrderDetailInline]

    def get_sub_total(self, obj):
        return obj.sub_total
    get_sub_total.short_description = _("Sub Total")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "distributor":
            kwargs["queryset"] = Distributor.objects.filter(is_online=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def clean(self, request, obj):
        if obj.status != 'pending' and not obj.distributor:
            raise ValidationError({
                'distributor': _('Se requiere un distribuidor cuando el estado no es "pending"')
            })

    def save_model(self, request, obj, form, change):
        try:
            self.clean(request, obj)
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form._errors.update(e.message_dict)
            return

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super().changeform_view(request, object_id, form_url, extra_context)
        except ValidationError as e:
            form = self.get_form(request)(request.POST)
            form._errors = e.message_dict
            context = self.get_changeform_initial_data(request)
            context.update(extra_context or {})
            return self.render_change_form(request, context, form=form, obj=None)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'get_final_price']
    readonly_fields = ['get_final_price']
    
    def get_final_price(self, obj):
        return obj.get_final_price()
    get_final_price.short_description = _("Precio Final")


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'id',
        'restaurant',
        'price',
        'um',
        'category',
        'rating',
        'is_active',
    ]
    list_filter = ['is_active']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            if request.GET.get('restaurant'):
                kwargs["queryset"] = ProductCategory.objects.filter(business_id=request.GET.get('restaurant'))
            else:
                kwargs["queryset"] = ProductCategory.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(RestaurantRating)
class RestaurantRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Metrics)


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(DashboardView.as_view()), name='admin_dashboard'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_dashboard'] = True
        return super().index(request, extra_context)

admin_site = CustomAdminSite(name='customadmin')
