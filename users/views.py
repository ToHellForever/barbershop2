from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import (
    CustomRegisterForm,
    CustomLoginForm,
    CustomPasswordChangeForm,
    CustomSetPasswordForm,
    CustomPasswordResetForm,
    UserProfileUpdateForm
)
from django.views.generic.edit import CreateView
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.views.generic import DetailView



from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Order
from users.models import CustomUser

# импорт Sum
from django.db.models import Sum

class CustomPasswordResetView(PasswordResetView):
    """
    1. Начало сброса пароля. Человек вводит емейл для сброса
    """

    template_name = "users_login_registr.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "password_reset_email.html"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        print(f"DEBUG: Отправка письма для сброса пароля на {email}")  # Отладочный вывод
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"DEBUG: Ошибки валидации: {form.errors}")  # Отладочный вывод
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Восстановление пароля"
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    2. Загляните в Emeil - вам ушло письмо с инструкциями
    """

    message = "Инструкции по восстановлению пароля отправлены на Email"
    operation_type = "Внимание!"

    template_name = "user_message.html"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    3. Вью где отображается форма восстановление пароля (можно попасть только через платформу 9 3\4
    ) - комбо <uidb64> + <token>
    """

    operation_type = "Сменить пароль"
    extra_context = {"operation_type": operation_type}
    form_class = CustomSetPasswordForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    4. Ура! Вы сбросили пароль!
    """

    template_name = "user_message.html"
    message = "Вы успешно сменили пароль!"
    operation_type = "Внимание!"
    extra_context = {
        "operation_type": operation_type,
        "message": message,
    }


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users_login_registr.html"
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Смена пароля"
        return context


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


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Профиль"
        return context
    
class UserProfileUpdateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "users_profile.html"
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Профиль"
        return context