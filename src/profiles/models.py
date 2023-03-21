from django.db import models
from src.tour.models import Tour
from src.users.models import User


class OrderTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tour_order")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_order")
    quantity = models.IntegerField(verbose_name="Количество людей")
    number = models.CharField(max_length=20, verbose_name="Номер")
    arranged_date = models.DateField(auto_now_add=True, verbose_name="Дата брони")
    way_of_payment = models.CharField(max_length=20, verbose_name="Способ оплаты")
    payment = models.ImageField(upload_to="media", verbose_name="Чек")

    def __str__(self):
        return f"{self.user}"
