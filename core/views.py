from django.shortcuts import render, HttpResponse
from .data import orders, masters

def landing(request):
    """
    Главная страница.
    Отображает шаблон landing.html.
    """
    return render(request, 'landing.html') 

def thanks(request):
    """
    Страница благодарности.
    Отображает шаблон thanks.html.
    """
    return render(request, 'thanks.html') 
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
    return render(request, 'orders_list.html', context)

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
        return render(request, 'order_detail.html', context)
    except StopIteration:  # Заказ не найден
        return HttpResponse(f'Заказ с id={order_id} не найден')