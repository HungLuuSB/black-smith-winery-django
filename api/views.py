from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from order.models import Order, OrderDetail
from shop.models import Product, Stock
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.views import View
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now, timedelta
from django.db.models import Q
import calendar
import json
# Create your views here.


class TopSellingCategoryChart(View):
    def get(self, request, *args, **kwargs):
        data = (
            OrderDetail.objects.values("product__category__name")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")[:6]
        )

        labels = [entry["product__category__name"] for entry in data]
        data = [entry["total_sold"] for entry in data]

        return JsonResponse(
            {
                "labels": labels,
                "data": data,
            }
        )


class OrderChart(View):
    def get(self, request, *args, **kwargs):
        time_filter = request.GET.get("filter", "30d")
        metric = request.GET.get("metric", "revenue")

        today = now().date()

        if time_filter == "7d":
            start_date = today - timedelta(days=6)
            trunc_func = TruncDay
            date_range = [start_date + timedelta(days=i) for i in range(7)]
            labels = [d.strftime("%d %b") for d in date_range]

        elif time_filter == "12m":
            start_date = today.replace(day=1) - relativedelta(months=11)
            trunc_func = TruncMonth
            date_range = [
                today.replace(day=1) - relativedelta(months=i)
                for i in reversed(range(12))
            ]
            labels = [d.strftime("%b %Y") for d in date_range]

        else:
            start_date = today - timedelta(days=29)
            trunc_func = TruncDay
            date_range = [start_date + timedelta(days=i) for i in range(30)]
            labels = [d.strftime("%d %b") for d in date_range]

        orders = (
            Order.objects.filter(created_at__date__gte=start_date)
            .annotate(period=trunc_func("created_at"))
            .values("period")
        )

        if metric == "revenue":
            orders = orders.annotate(value=Sum("grand_total"))
        else:
            orders = orders.annotate(value=Count("id"))

        orders = orders.order_by("period")

        data_map = {
            entry["period"]
            .date()
            .replace(
                day=1 if trunc_func == TruncMonth else entry["period"].date().day
            ): entry["value"]
            for entry in orders
        }

        if trunc_func == TruncMonth:
            data = [data_map.get(month.replace(day=1), 0) for month in date_range]
        else:
            data = [data_map.get(day, 0) for day in date_range]

        return JsonResponse(
            {
                "labels": labels,
                "data": data,
            }
        )


class TotalOrdersChart(View):
    def get(self, request, *args, **kwargs):
        pass


def get_product_by_name(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "id")
    order = request.GET.get("order", "asc")
    page_number = request.GET.get("page", 1)

    sort_fields = {"id", "name", "price"}
    if sort not in sort_fields:
        sort = "id"

    order_prefix = "" if order == "asc" else "-"
    ordering = f"{order_prefix}{sort}"

    products = Product.objects.filter(Q(name__icontains=query)).order_by(ordering)

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)

    html = render_to_string("api/product_table.html", {"products": page_obj})
    pagination_html = render_to_string(
        "api/pagination_controls.html", {"page_obj": page_obj}
    )

    return JsonResponse({"table_html": html, "pagination_html": pagination_html})


def get_order_by_customer_name(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "id")
    order = request.GET.get("order", "asc")
    page_number = request.GET.get("page", 1)

    sort_fields = {"id", "name", "price"}
    if sort not in sort_fields:
        sort = "id"

    order_prefix = "" if order == "asc" else "-"
    ordering = f"{order_prefix}{sort}"

    orders = Order.objects.filter(Q(customer_last_name__icontains=query)).order_by(
        ordering
    )

    paginator = Paginator(orders, 10)
    page_obj = paginator.get_page(page_number)

    html = render_to_string("api/order_table.html", {"orders": page_obj})
    pagination_html = render_to_string(
        "api/pagination_controls.html", {"page_obj": page_obj}
    )

    return JsonResponse({"table_html": html, "pagination_html": pagination_html})
