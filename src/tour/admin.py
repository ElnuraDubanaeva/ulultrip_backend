from django.contrib import admin
from .models import Tour, Category, Region, Review, Images, Guide, AboutUs


# Register your models here.
class ImagesModel(admin.StackedInline):
    model = Images


class TourAdmin(admin.ModelAdmin):
    inlines = [ImagesModel]
    search_fields = "title description".split()
    list_display_links = ["title"]
    list_display = "title price date_departure actual_limit complexity duration average_rating".split()
    list_editable = "price date_departure".split()
    ordering = ["date_departure"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 10
    list_filter = (
        "region category date_departure is_hot duration complexity guide".split()
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class GuideAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ReviewAdmin(admin.ModelAdmin):
    search_fields = "author post".split()
    list_display = "author post rating date_published".split()
    ordering = ["rating"]
    list_filter = "date_published rating".split()
    list_per_page = 10


class AboutUsAdmin(admin.ModelAdmin):
    model = AboutUs

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()

        if num_objects >= 1:
            return False
        return True


admin.site.register(Tour, TourAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Images)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Guide, GuideAdmin)
