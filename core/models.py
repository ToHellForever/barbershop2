from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField('Service', related_name="provided_by", verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("completed", "Выполненная"), 
        ("canceled", "Отменена"),  
    )

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new", verbose_name="Статус")  
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Мастер")  
    services = models.ManyToManyField('Service', related_name='orders', verbose_name="Услуги")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"{self.client_name} - {self.appointment_date}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self):
        
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
class Review(models.Model):
    RATING_CHOICES = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )
    STATUS_CHOICES = (
        ("new", "Новый"),
        ("ai_moderated", "На модерации"),
        ("ai_approved", "Одобрен AI"),
        ("ai_rejected", "Отклонен AI"),
        ("published", "Опубликован"),
        ("archived", "В архиве"),
    )
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, default=None, verbose_name="Имя клиента")
    master = models.ForeignKey('Master', on_delete=models.SET_NULL, verbose_name="Мастер", related_name="reviews", null=True)
    photo = models.ImageField(upload_to="reviews/", null=True, blank=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5, verbose_name="Рейтинг")
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20, verbose_name="Статус")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    def __str__(self):
        return f"Отзыв от {self.client_name} о {self.master}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"