from src.users.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from src.users.utils import path_and_rename
import string
import random


class Guide(models.Model):
    class Meta:
        verbose_name = "Guide"
        verbose_name_plural = "Guides"

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="media/guides", blank=True)
    slug = models.SlugField(unique=True)

    def get_initials(self):
        return f"{self.name} {self.surname}"

    def __str__(self):
        return self.get_initials()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_author"
    )
    post = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="tour_reviews"
    )
    rating = models.SmallIntegerField(choices=RATING_CHOICES, default=5)
    date_published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Region(models.Model):
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    images = models.FileField(
        upload_to=path_and_rename,
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "img", "jpg", "jpeg"])
        ],
    )
    tour = models.ForeignKey(
        "Tour", on_delete=models.CASCADE, related_name="tour_images"
    )
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return str(self.images)


class Tour(models.Model):
    class Meta:
        verbose_name = "Tour"
        verbose_name_plural = "Tours"

    DURATION_CHOICES = (("1", "День"), ("3", "3 дня"), ("7", "7 дней"))

    COMPLEXITY_CHOICES = (
        ("Easy", "Легкий"),
        ("Medium", "Средний"),
        ("Hard", "Тяжелый"),
        ("Extra", "Экстра"),
    )

    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.SmallIntegerField("Цена")
    slug = models.SlugField(unique=True)
    date_published = models.DateField(auto_now=True)
    date_departure = models.DateField()
    date_arrival = models.DateField()
    region = models.ManyToManyField(Region, related_name="tour_region")
    quantity_limit = models.PositiveIntegerField()
    actual_limit = models.PositiveIntegerField(editable=False, blank=True, null=True)
    is_hot = models.BooleanField(default=False)
    duration = models.CharField(max_length=255, choices=DURATION_CHOICES)
    complexity = models.CharField(max_length=255, choices=COMPLEXITY_CHOICES)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    qr_code = models.CharField(default="", max_length=8, blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        count = self.tour_reviews.count()
        if count == 0:
            return f"No reviews yet"
        total = 0
        for i in self.tour_reviews.all():
            total += i.rating
        return total / count

    def save(self, *args, **kwargs):
        strings_upp = string.ascii_uppercase
        strings_low = string.ascii_lowercase
        digits = string.digits
        str_up = "".join(random.choice(strings_upp) for i in range(2))
        str_low = "".join(random.choice(strings_low) for i in range(2))
        dig_ = "".join(random.choice(digits) for i in range(4))
        self.qr_code = str_up + dig_ + str_low
        return super(Tour, self).save(*args, **kwargs)


class AboutUs(models.Model):
    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    specialists = models.PositiveSmallIntegerField()
    clients = models.PositiveSmallIntegerField()
    tours = models.PositiveSmallIntegerField()
    years = models.PositiveSmallIntegerField()
