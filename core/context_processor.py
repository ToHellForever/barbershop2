from django.urls import reverse
def menu_items(request):
    return {
        'menu_items': [
            {'name': 'Главная', 'url': reverse('landing')},
            {'name': 'Заказы', 'url': reverse('orders_list')},
        ]
    }