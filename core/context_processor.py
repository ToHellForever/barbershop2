from django.urls import reverse

def menu_items(request):
    menu = [
        {'name': 'Главная', 'url': reverse('landing'), 'staff_only': False},
        {'name': 'Наши услуги', 'url': reverse('services_views'), 'staff_only': False},
        {'name': 'Записаться', 'url': reverse('order_create'), 'staff_only': False},
        {'name': 'Оставить отзыв', 'url': reverse('review_create'), 'staff_only': False},
    ]   

    if request.user.is_authenticated and request.user.is_staff:
        menu.append({'name': 'Заказы', 'url': reverse('orders_list'), 'staff_only': True})
    
    return {'menu_items': menu}