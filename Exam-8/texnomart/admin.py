from django.contrib import admin
from texnomart.models import Category, Product, Comment, Image, Attribute, AttributeValue, ProductAttribute
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name',)}

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug']
    prepopulated_fields = {'slug': ('product_name',)}


# admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.unregister(Group)
