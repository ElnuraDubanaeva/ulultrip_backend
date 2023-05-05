from django.db import models
from django.core.validators import FileExtensionValidator

from src.users.utils import path_and_rename
from .services import TourServices
from src.users.models import User
from .constants import TourConstants


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
    rating = models.SmallIntegerField(choices=TourConstants.RATING_CHOICES, default=5)
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
    duration = models.CharField(max_length=255, choices=TourConstants.DURATION_CHOICES)
    complexity = models.CharField(
        max_length=255, choices=TourConstants.COMPLEXITY_CHOICES
    )
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
        self.qr_code = TourServices.make_qr_code()
        return super(Tour, self).save(*args, **kwargs)


class AboutUs(models.Model):
    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    specialists = models.PositiveSmallIntegerField()
    clients = models.PositiveSmallIntegerField()
    tours = models.PositiveSmallIntegerField()
    years = models.PositiveSmallIntegerField()
