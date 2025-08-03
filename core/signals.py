from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Review, Order
from .telegram_bot import send_telegram_message
from django.conf import settings
import asyncio

api_key = settings.TELEGRAM_BOT_API_KEY
user_id = settings.TELEGRAM_USER_ID

@receiver(m2m_changed, sender=Order.services.through)
def notify_telegram_on_order_create(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для модели Order.
    Он обрабатывает добавление КАЖДОЙ услуги в запись на консультацию.
    """
    print("notify_telegram_on_order_create function called")
    try:
        if action == 'post_add' and kwargs.get('pk_set'):
            list_services = [service.name for service in instance.services.all()]
            appointment_date = instance.appointment_date.strftime("%d.%m.%Y") if instance.appointment_date else "Не указана"
            tg_markdown_message = f"""

====== *Новый заказ!* ======
**Имя:** {instance.client_name}
**Телефон:** {instance.phone}
**Мастер:** {instance.master.name}
**Дата записи:** {appointment_date}
**Услуги:** {', '.join(list_services)}
**Комментарий:** {instance.comment}

**Подробнее:** http://127.0.0.1:8000/admin/core/order/{instance.id}/change/

#заказ 

"""
            asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")

