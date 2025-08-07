from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Master, Review, Order, Service
from .forms import OrderForm, ReviewForm

# безопасность
from django.contrib.auth.decorators import login_required

# импорт q
from django.db.models import Q, Sum, Count, F

# импорт классовых views
from django.views.generic import TemplateView, ListView, DetailView, CreateView

# импорт reverse_lazy
from django.urls import reverse_lazy, reverse


def get_master_services(request):
    """
    Функция для получения списка услуг для конкретного мастера.
    для использования в AJAX-запросе
    """
    master_id = request.GET.get("master_id")
    services = []
    if master_id:
        try:
            master = Master.objects.get(id=master_id)
            services = list(master.services.values("id", "name"))
        except Master.DoesNotExist:
            pass
    return JsonResponse({"services": services})


class LandingView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["masters"] = Master.objects.filter(is_active=True)
        context["reviews"] = (
            Review.objects.select_related("master")
            .filter(is_published=True)
            .order_by("-created_at")[:3]
        )
        return context


def services_views(request):
    """
    Страница услуг.
    Отображает шаблон services.html, передавая данные об услугах.
    """
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "services_views.html", context=context)


class ThanksView(TemplateView):
    """View для страницы благодарности"""

    template_name = "thanks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Спасибо"
        context["messages"] = "Спасибо за ваше обращение"

        # Добавляем специфические сообщения в зависимости от источника
        source = kwargs.get("source", "")
        if source == "order_create":
            context["messages"] = "Спасибо за заказ! Мы скоро с вами свяжемся."
        elif source == "review_create":
            context["messages"] = (
                "Спасибо за ваш отзыв! Ваше мнение очень важно для нас."
            )

        context["source"] = source
        return context


class OrdersListView(ListView):
    model = Order
    template_name = "orders_list.html"
    context_object_name = "orders"
    ordering = ['-date_created'] 

    def get_queryset(self):
        query_set = super().get_queryset()
        search_query = self.request.GET.get("q", "")
        search_name = self.request.GET.get("search_name", "")
        search_phone = self.request.GET.get("search_phone", "")
        search_comment = self.request.GET.get("search_comment", "")
        q_object = Q()
        if search_query:
            if search_name == "on":
                q_object |= Q(client_name__icontains=search_query)
            if search_phone == "on":
                q_object |= Q(phone__icontains=search_query)
            if search_comment == "on":
                q_object |= Q(comment__icontains=search_query)
        return query_set.filter(q_object)


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset.select_related("master")
            .prefetch_related("services")
            .annotate(total_price=Sum("services__price"))
        )    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = self.object.services.all()
        return context

class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name = "order_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "order_create"})
    success_message = "Заказ успешно создан!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании заказа!")
        return super().form_invalid(form)


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_class_form.html"
    success_url = reverse_lazy("thanks", kwargs={"source": "review_create"})
    success_message = "Отзыв успешно создан!"

    def form_valid(self, form):
        form.instance.status = "new"
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании заказа!")
        return super().form_invalid(form)
