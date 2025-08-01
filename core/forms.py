from django import forms
from .models import Order, Review
from django.utils import timezone
from datetime import datetime


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].initial = 5

    class Meta:
        model = Review
        fields = ["client_name", "text", "rating", "master", "photo"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
            "text": forms.Textarea(attrs={"class": "form-control", "placeholder": "Ваш отзыв", "rows": 3}),
            "rating": forms.Select(attrs={"class": "form-control", "placeholder": "Оценка"}),
            "master": forms.Select(attrs={"class": "form-control", "placeholder": "Выберите мастера"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["client_name", "phone", "comment", "master", "appointment_date", "services"]
        widgets = {
            "client_name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Комментарий к заказу",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "master": forms.Select(attrs={"class": "form-control js-master-select"}),
            "services": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
            "appointment_date": forms.DateInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get("appointment_date")
        master = self.cleaned_data.get("master")
        today = timezone.now().date()
        if hasattr(appointment_date, "date"):
            appointment_date_date = appointment_date.date()
        else:
            appointment_date_date = appointment_date
        if appointment_date_date < today:
            raise forms.ValidationError("Вы не можете записаться на прошедшую дату.")
        # Проверка занятости
        if master and appointment_date:
            exists = Order.objects.filter(master=master, appointment_date=appointment_date).exists()
            if exists:
                raise forms.ValidationError("На выбранную дату и время у этого мастера уже есть запись.")
        return appointment_date

    def clean_services(self):
        services = self.cleaned_data.get("services")
        master = self.cleaned_data.get("master")
        if not master:
            raise forms.ValidationError("Выберите мастера для заказа.")

        if not services:
            raise forms.ValidationError("Выберите хотя бы одну услугу для заказа.")
        # все услуги которые предоставляет мастер
        master_services = master.services.all()

        not_approved_services = []
        for service in services:
            if service not in master_services:
                not_approved_services.append(service.name)

        if not_approved_services:
            raise forms.ValidationError(
                f"Услуги {', '.join(not_approved_services)} не предоставляются мастером {master.name}."
            )
        return services