from django.shortcuts import render
from order.models import Order
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime
import calendar
import json
# Create your views here.
def sales_chart(request):
    months = list(calendar.month_name)[1:]
    orders_by_month = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    sales_data = {
        order['month'].month: order['total']
        for order in orders_by_month
    }

    data = [sales_data.get(month, 0) for month in range(1, 13)]

    
    return JsonResponse({
        'labels': months,
        'data': data,
    })