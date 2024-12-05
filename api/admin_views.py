from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, FloatField
from django.db.models.functions import Cast
from django.utils import timezone
from datetime import timedelta
from .models import Order, Restaurant, Product, OrderDetail

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)

        # Cantidad de órdenes pendientes
        pending_orders_count = Order.objects.filter(status='pending').count()

        # Dinero total de ventas del día con porcentaje dinámico
        daily_sales = OrderDetail.objects.filter(
            order__status='delivered',
            order__date__range=(today_start, today_end)
        ).annotate(
            commission=ExpressionWrapper(
                F('unit_price') * F('quantity') * Cast('tax_rate', FloatField()) / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).aggregate(
            total=Sum('commission')
        )['total'] or 0

        # Dinero total de ventas de la semana
        weekly_sales = OrderDetail.objects.filter(
            order__status='delivered',
            order__date__range=(week_start, now)
        ).annotate(
            commission=ExpressionWrapper(
                F('unit_price') * F('quantity') * Cast('tax_rate', FloatField()) / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).aggregate(
            total=Sum('commission')
        )['total'] or 0

        # Dinero total de ventas del mes
        monthly_sales = OrderDetail.objects.filter(
            order__status='delivered',
            order__date__range=(month_start, now)
        ).annotate(
            commission=ExpressionWrapper(
                F('unit_price') * F('quantity') * Cast('tax_rate', FloatField()) / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).aggregate(
            total=Sum('commission')
        )['total'] or 0

        # Top restaurantes y productos
        top_restaurants = Restaurant.objects.annotate(
            total_sales=Sum(
                F('product__orderdetail__unit_price') * F('product__orderdetail__quantity')
            ),
            total_orders=Count('product__orderdetail__order', distinct=True),
            commission=ExpressionWrapper(
                F('product__orderdetail__unit_price') * 
                F('product__orderdetail__quantity') * 
                Cast('tax', FloatField()) / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).filter(
            total_sales__isnull=False
        ).order_by('-total_sales')[:10]

        top_products = Product.objects.annotate(
            total_sold=Sum('orderdetail__quantity'),
            total_revenue=ExpressionWrapper(
                F('orderdetail__unit_price') * 
                F('orderdetail__quantity') * 
                Cast('restaurant__tax', FloatField()) / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).filter(
            total_sold__isnull=False
        ).order_by('-total_sold')[:10]

        context.update({
            'pending_orders_count': pending_orders_count,
            'daily_sales': daily_sales,
            'weekly_sales': weekly_sales,
            'monthly_sales': monthly_sales,
            'top_restaurants': top_restaurants,
            'top_products': top_products,
        })
        return context