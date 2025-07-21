from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_detail, services_views, masters_views, entry_form
from core import views


urlpatterns = [
    path('admin/', admin.site.urls), # Административная панель Django
    path('', views.landing, name='landing'),  # Главная страница
    path('orders/', views.orders_list, name='orders_list'),  # Список заказов
    path('thanks/', views.thanks, name='thanks'),  # Страница благодарности
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),  # Детали заказа
    path('services/', views.services_views, name='services'), # Список услуг
    path('masters/', views.masters_views, name='masters'), # Список мастеров
    path('entry_form/', views.entry_form, name='entry_form'), # Форма записи
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)