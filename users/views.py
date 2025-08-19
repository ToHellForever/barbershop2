from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import (
    CustomRegisterForm,
    CustomLoginForm,
)
from django.views.generic.edit import CreateView
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
)
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Order

# импорт Sum
from django.db.models import Sum


class CustomRegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно зарегистрировались! Добро пожаловать!"

    def form_valid(self, form):
        # 1. Сохраняем пользователя. Теперь у объекта user есть ID.
        user = form.save()

        # 2. Устанавливаем self.object, как того требует CreateView.
        self.object = user

        # 3. Теперь безопасно вызываем login().
        login(self.request, user)

        messages.success(self.request, self.success_message)

        # 4. Выполняем перенаправление.
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка регистрации. Пожалуйста, проверьте введенные данные."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Регистрация"
        return context


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")
    success_message = "Вы успешно авторизовались!"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при авторизации!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Авторизация"
        return context


class CustomLogoutView(LogoutView):
    next_page = "/"
    success_message = "Вы успешно разлогинились!"

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        orders = Order.objects.filter(client_name=self.request.user.username).order_by(
            "-date_created"
        )
        for order in orders:
            order.total_price = (
                order.services.aggregate(total=Sum("price"))["total"] or 0
            )
        context["orders"] = orders
        return context
