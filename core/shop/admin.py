# from django.contrib import admin
# from .models import ProductModel, ProductImageModel, ProductCategoryModel,WishlistProductModel

# # Register your models here.

# @admin.register(ProductModel)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "stock", "status","price","discount_percent", "created_date")

# @admin.register(ProductCategoryModel)
# class ProductCategoryModelAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "created_date")

# @admin.register(ProductImageModel)
# class ProductImageModelAdmin(admin.ModelAdmin):
#     list_display = ("id", "file", "created_date")

# @admin.register(WishlistProductModel)
# class WishlistProductModelAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "product")


from django.contrib import admin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, WishlistProductModel
from django.utils.html import format_html

# ثبت مدل ProductModel در پنل ادمین
@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "stock", "status", "price", "discount_percent", "created_date")
    search_fields = ("title",)  # جستجو بر اساس عنوان محصول
    list_filter = ("status", "created_date")  # فیلتر بر اساس وضعیت محصول و تاریخ ایجاد
    prepopulated_fields = {"slug": ("title",)}  # پر کردن خودکار فیلد slug از عنوان محصول

# ثبت مدل ProductCategoryModel در پنل ادمین
@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")
    search_fields = ("title",)  # جستجو بر اساس عنوان دسته‌بندی
    list_filter = ("created_date",)  # فیلتر بر اساس تاریخ ایجاد

# ثبت مدل ProductImageModel در پنل ادمین
@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "thumbnail", "created_date")
    
    # متد سفارشی برای نمایش تصویر بندانگشتی در پنل ادمین
    def thumbnail(self, obj):
        if obj.file:
            return format_html('<img src="{}" width="50" height="50" />', obj.file.url)
        return "-"
    thumbnail.short_description = "Thumbnail"  # عنوان برای ستون نمایش تصویر بندانگشتی

# ثبت مدل WishlistProductModel در پنل ادمین
@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
    search_fields = ("user__username", "product__title")  # جستجو بر اساس نام کاربر و عنوان محصول
