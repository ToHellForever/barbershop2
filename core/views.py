from django.shortcuts import render, HttpResponse
from .data import orders, masters, services
from .models import Master, Review
# безопасность 
from django.contrib.auth.decorators import login_required



def landing(request):
    """
    Главная страница.
    Отображает шаблон landing.html, передавая данные о мастерах и отзывах.
    """
    masters = Master.objects.filter(is_active=True) # Получаем активных мастеров
    reviews = Review.objects.filter(is_published=True).order_by('-created_at')[:6] # Получаем последние 6 опубликованных отзывов

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
    context = {
        'services': services
        }
    return render(request, 'services.html', context=context)

def masters_views(request):
    """
    Страница мастеров.
    Отображает шаблон masters.html, передавая данные о мастерах.
    """
    context = {
        'masters': masters
        }
    return render(request, 'masters.html', context=context)

def entry_form(request):
    """
    Страница записи на услугу.
    Отображает шаблон entry.html, передавая данные о мастерах и услугах для выбора.
    """
    context = {
        'services': services,
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
    Отображает шаблон orders_list.html, передавая данные о заказах.
    """
    # Создаем словарь, связывающий master_id с master_name
    master_dict = {master["id"]: master["name"] for master in masters}

    # Добавляем master_name в каждый заказ
    for order in orders:
        order["master_name"] = master_dict.get(order["master_id"], "Неизвестный мастер")
    # Передаем данные о заказах в контекст
    context = {'orders': orders}  
    return render(request, 'orders_list.html', context=context)

@login_required
def order_detail(request, order_id):
    """
    Страница деталей заказа.
    Отображает шаблон order_detail.html, передавая данные о конкретном заказе.
    Если заказ не найден, возвращает HttpResponse с сообщением об ошибке.
    """
    # Создаем словарь, связывающий master_id с master_name
    master_dict = {master["id"]: master["name"] for master in masters}
    try:
        # Попытка найти заказ с заданным ID
        order = next(order for order in orders if order['id'] == order_id)
        # Добавляем master_name в заказ
        order["master_name"] = master_dict.get(order["master_id"], "Неизвестный мастер")
        # Передаем данные о заказах в контекст
        context = {'order': order}
        return render(request, 'order_detail.html', context=context)
    except StopIteration:  # Заказ не найден
        return HttpResponse(f'Заказ с id={order_id} не найден')