from django.contrib import admin
from .models import Category, Product
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    def upload_thumb(self, obj):
        try:
            img = mark_safe('<img src="%s" width="50px" />' % (obj.thumb.url,))
        except Exception as e:
            img = ''
        return img

    upload_thumb.short_description = 'Thumb Preview'
    upload_thumb.allow_tags = True

    fields = ('category', 'name', 'slug', 'price', 'description', 'available', 'image', 'thumb', 'upload_thumb',)
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'upload_thumb']
    readonly_fields = ('thumb', 'upload_thumb',)
    list_filter = ['available', 'created', 'updated']
    prepopulated_fields = {'slug': ('name',)}


admin.site.site_header = 'Orwell Cyberspace Administration'
admin.site.site_title = 'Orwell'
