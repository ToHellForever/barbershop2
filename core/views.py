from django.shortcuts import render, get_object_or_404
from .models import Master, Review, Order, Service
# безопасность 
from django.contrib.auth.decorators import login_required



def landing(request):
    """
    Главная страница.
    Отображает шаблон landing.html, передавая данные о мастерах и отзывах.
    """
    masters = Master.objects.filter(is_active=True) # Получаем активных мастеров
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:4] # Получаем последние 4 отзыва

    context = {
        'masters': masters,
        'reviews': reviews,
    }
    return render(request, 'landing.html', context=context)

def services_views(request):
    """
    Страница услуг.
    Отображает шаблон services.html, передавая данные об услугах.
    """
    services = Service.objects.all() 
    context = {
        'services': services
    }
    return render(request, 'services.html', context=context)


def masters_views(request):
    """
    Страница мастеров.
    Отображает шаблон masters.html, передавая данные о мастерах.
    """
    masters = Master.objects.all() 
    context = {
        'masters': masters
    }
    return render(request, 'masters.html', context=context)


def entry_form(request):
    """
    Страница записи на услугу.
    Отображает шаблон entry.html, передавая данные о мастерах и услугах для выбора.
    """
    services = Service.objects.all()
    masters = Master.objects.filter(is_active=True) # только активные мастера на будущее 
    context = {
        'services': services,
        'masters': masters
    }
    return render(request, 'entry_form.html', context=context)

def thanks(request):
    """
    Страница благодарности.
    Отображает шаблон thanks.html.
    """
    return render(request, 'thanks.html') 


@login_required
def orders_list(request):
    """
    Список заказов.
    Отображает шаблон orders_list.html, передавая данные о заказах, отсортированных по дате создания.
    """
    # Получаем все заказы из базы данных, сортируем по убыванию date_created
    orders = Order.objects.all().order_by('-date_created')

    master_dict = {master.id: master.name for master in Master.objects.all()}

    for order in orders:
        order.master_name = master_dict.get(order.master_id, "Неизвестный мастер")

    context = {'orders': orders}
    return render(request, 'orders_list.html', context=context)


@login_required
def order_detail(request, order_id):
    """
    Страница деталей заказа.
    Отображает шаблон order_detail.html, передавая данные о конкретном заказе.
    Если заказ не найден, возвращает 404 ошибку.
    """
    # Получаем заказ из базы данных по ID заказа или возвращает 404 ошибку, если заказ не найден
    order = get_object_or_404(Order, pk=order_id)

    # Получаем имя мастера
    master_name = order.master.name if order.master else "Неизвестный мастер"


    related_services = order.services.all() 

    context = {
        'order': order,
        'master_name': master_name, 
        'related_services': related_services 
    }
    return render(request, 'order_detail.html', context=context)