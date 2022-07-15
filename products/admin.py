from django.contrib import admin

from products.models import Brand, Product, SneakersType, CommentRating, Image, Like, Favorites


class ImageItemsInline(admin.TabularInline):
    model = Image
    extra = 0

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'size']
    inlines = [ImageItemsInline]


admin.site.register(Product, ImageAdmin)
admin.site.register(SneakersType)
admin.site.register(Brand)
admin.site.register(CommentRating)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Favorites)