from django.urls import reverse

def menu_items(request):
    menu = [
        {'name': 'Главная', 'url': reverse('landing'), 'staff_only': False},
        {'name': 'Записаться', 'url': reverse('entry_form'), 'staff_only': False},
    ]

    if request.user.is_authenticated and request.user.is_staff:
        menu.append({'name': 'Заказы', 'url': reverse('orders_list'), 'staff_only': True})

    return {'menu_items': menu}