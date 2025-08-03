from django.contrib import admin
from .models import Master, Order, Service, Review
from django.db.models import Sum
import datetime
from django.utils import timezone

# Инлайн для отзывов на странице мастера
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("client_name", "text", "rating", "is_published", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True
    
# Кастомный фильтр по общей сумме заказа
class TotalOrderPrice(admin.SimpleListFilter):
    title = "По общей сумме заказа"
    parameter_name = "total_order_price"

    def lookups(self, request, model_admin):
        return (
            ("one_thousand", "До 1000 рублей"),
            ("three_thousand", "До 3000 рублей"),
            ("five_thousand", "До 5000 рублей"),
            ("up_five_thousand", "Более 5000 рублей"),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(total_price_agg=Sum("services__price"))
        if self.value() == "one_thousand":
            return queryset.filter(total_price_agg__lt=1000)
        elif self.value() == "three_thousand":
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=3000)
        elif self.value() == "five_thousand":
            return queryset.filter(total_price_agg__gte=3000, total_price_agg__lt=5000)
        elif self.value() == "up_five_thousand":
            return queryset.filter(total_price_agg__gte=5000)
        return queryset
# Кастомный фильтр по дате записи
class AppointmentDateFilter(admin.SimpleListFilter):
    title = "По дате записи"
    parameter_name = "appointment_date"

    def lookups(self, request, model_admin):
        return (
            ("today", "Сегодня"),
            ("tomorrow", "Завтра"),
            ("this_week", "На этой неделе"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        today = now.date()
        if self.value() == 'today':
            return queryset.filter(appointment_date__date=today)
        elif self.value() == 'tomorrow':
            tomorrow = today + datetime.timedelta(days=1)
            return queryset.filter(appointment_date__date=tomorrow)
        elif self.value() == 'this_week':
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            return queryset.filter(appointment_date__date__range=(start_of_week, end_of_week))
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_name",
        "phone",
        "master",
        "appointment_date",
        "status",
        "total_price",
    )
    list_filter = (
        "status",
        "master",
        TotalOrderPrice,
        AppointmentDateFilter,
    )
    search_fields = (
        "client_name",
        "phone",
    )
    list_editable = ("status",)
    filter_horizontal = ("services",)
    actions = ("mark_completed", "mark_canceled", "mark_new", "mark_confirmed")

    @admin.action(description="Отметить как выполненные")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить как отменённые")
    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Отметить как новые")
    def mark_new(self, request, queryset):
        queryset.update(status="new")

    @admin.action(description="Отметить как подтверждённые")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    @admin.display(description="Общая сумма")
    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        
        
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "experience",
        "is_active",
        "service_count",
    )
    list_filter = ("is_active", "services")
    search_fields = ("name",)
    filter_horizontal = ("services",)
    inlines = [ReviewInline]

    @admin.display(description="Количество услуг")
    def service_count(self, obj):
        return obj.services.count()

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        
        
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration",
        "is_popular",
    )
    search_fields = ("name",)
    list_filter = ("is_popular",)
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "master",
        "text",
        "rating",
        "is_published",
        "created_at",
    )
    list_filter = ("is_published", "master")
    search_fields = ("client_name", "text")
    readonly_fields = ("created_at",)
    actions = ("publish_reviews", "unpublish_reviews")
    list_editable = ("is_published",)
    created_at = ("created_at",)
    
    class Media:
        css = {
            'all': ('css/admin.css',)
        }