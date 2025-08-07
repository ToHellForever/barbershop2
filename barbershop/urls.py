from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import (
    LandingView,
    ThanksView,
    OrdersListView,
    OrderDetailView,
    services_views,
    ReviewCreateView,
    OrderCreateView,
)
from core.views import get_master_services
from core import views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),  # Административная панель Django
    path("", views.LandingView.as_view(), name="landing"),  # Главная страница
    path("orders/", views.OrdersListView.as_view(), name="orders_list"),  # Список заказов
    path("thanks/<str:source>/", views.ThanksView.as_view(), name="thanks"),  # Страница благодарности
    path("orders/<int:order_id>/", views.OrderDetailView.as_view(), name="order_detail"),  # Детали заказа
    path("services/", views.services_views, name="services_views"),  # Список услуг
    path("order_create/", views.OrderCreateView.as_view(), name="order_create"),  # Страница записи на услугу
    path("review_create/", views.ReviewCreateView.as_view(), name="review_create"),  # Создание отзыва
] + debug_toolbar_urls()

# API для динамической подгрузки услуг мастера
urlpatterns += [
    path("api/master_services/", get_master_services, name="get_master_services"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
