from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import landing, thanks, thanks_form, orders_list, order_detail, services_views, masters_views, order_page, review_create, order_create
from core.views import get_master_services
from core import views
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls), # Административная панель Django
    path('', views.landing, name='landing'),  # Главная страница
    path('orders/', views.orders_list, name='orders_list'),  # Список заказов
    path('thanks/', views.thanks, name='thanks'),  # Страница благодарности
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),  # Детали заказа
    path('services/', views.services_views, name='services'), # Список услуг
    path('masters/', views.masters_views, name='masters'), # Список мастеров
    path('order_page/', views.order_page, name='order_page'),  # Страница записи на услугу
    path('order_create/',  views.order_create, name='order_create'), #Страница записи на услугу 
    path('review_create/', views.review_create, name='review_create'),  # Создание отзыва
    path('thanks_form/', views.thanks_form, name='thanks_form')
] + debug_toolbar_urls()

# API для динамической подгрузки услуг мастера
urlpatterns += [
    path('api/master_services/', get_master_services, name='get_master_services'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)