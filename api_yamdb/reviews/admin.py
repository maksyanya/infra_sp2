from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE
from reviews.models import Category, Genre, Title


@admin.register(Genre)
class GenreAmdin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    list_filter = ('category',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE
