from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Master, Review, Order, Service
from .forms import OrderForm, ReviewForm
# безопасность 
from django.contrib.auth.decorators import login_required
# импорт q
from django.db.models import Q, Sum

def get_master_services(request):
    master_id = request.GET.get('master_id')
    services = []
    if master_id:
        try:
            master = Master.objects.get(id=master_id)
            services = list(master.services.values('id', 'name'))
        except Master.DoesNotExist:
            pass
    return JsonResponse({'services': services})

def landing(request):
    """
    Главная страница.
    Отображает шаблон landing.html, передавая данные о мастерах и отзывах.
    """
    masters = Master.objects.filter(is_active=True) # Получаем активных мастеров
    reviews = Review.objects.select_related('master').filter(is_published=True).order_by('-created_at')[:4] # Получаем последние 4 отзыва

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

def thanks(request):
    """
    Страница благодарности.
    Отображает шаблон thanks.html.
    """
    return render(request, 'thanks.html') 

def thanks_form(request):
    """
    Страница благодарности после оставления отзыва
    """
    return render(request, 'thanks_form.html')

@login_required
def orders_list(request):
    search_query = request.GET.get('q', '')  # Получаем поисковый запрос
    search_name = request.GET.get('search_name', 'on')  # По умолчанию включен
    search_phone = request.GET.get('search_phone', '')
    search_comment = request.GET.get('search_comment', '')

    # Создаем базовый QuerySet, отсортированный по дате создания
    orders = Order.objects.all().order_by('-date_created')

    # Создаем Q-объект для фильтрации
    q_object = Q()

    # Если есть поисковый запрос, добавляем условия в зависимости от чекбоксов
    if search_query:
        if search_name == 'on':  # Если включен чекбокс "Имя клиента"
            q_object |= Q(client_name__icontains=search_query)
        if search_phone == 'on':  # Если включен чекбокс "Телефон"
            q_object |= Q(phone__icontains=search_query)
        if search_comment == 'on':  # Если включен чекбокс "Комментарий"
            q_object |= Q(comment__icontains=search_query)

        # Фильтруем заказы с использованием Q-объекта
        orders = Order.objects.prefetch_related('services').select_related('master').filter(q_object)
    context = {
        'orders': orders,
        'search_query': search_query,
        'search_name': search_name,
        'search_phone': search_phone,
        'search_comment': search_comment,
    }
    return render(request, 'orders_list.html', context=context)


@login_required
def order_detail(request, order_id):
    """
    Страница деталей заказа.
    Отображает шаблон order_detail.html, передавая данные о конкретном заказе.
    Если заказ не найден, возвращает 404 ошибку.
    """
    # Получаем заказ по ID, используя prefetch_related и select_related для оптимизации запросов
    # Используем annotate для получения суммы стоимости услуг
    order = (
        Order.objects.prefetch_related("services")
        .select_related("master")
        .annotate(total_price=Sum("services__price"))
        .get(id=order_id)
    )

    # Получаем имя мастера
    master_name = order.master.name if order.master else "Неизвестный мастер"

    # Получаем связанные услуги
    related_services = order.services.all() 

    context = {
        'order': order,
        'master_name': master_name, 
        'related_services': related_services,
        'phone': order.phone,  
        'comment': order.comment,  
        'appointment_date': order.appointment_date, 
        'date_created': order.date_created,
    }
    return render(request, 'order_detail.html', context=context)

def order_page(request):
    form = OrderForm()
    return render(request, "order_page.html", {"form": form})

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()

    return render(request, "order_page.html", {"form": form})


def review_create(request):
    if request.method == "GET":
        form = ReviewForm()
        return render(request, "review_class_form.html", {'form': form})

    elif request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("thanks_form")
        else:
            return render(request, "review_class_form.html", {'form': form})