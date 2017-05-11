# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from books.models import Book, Author, Language, Genre, Award
from grappelli_filters.admin import FiltersMixin
from grappelli_filters.filters import RelatedFkAutocompleteFilter, \
    RelatedM2mAutocompleteFilter
from utils import str_list_of_objects


@admin.register(Book)
class BookAdmin(FiltersMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = (
        'title',
        'author',
        'language',
        'publication_date',
        'genres_list',
        'awards_list',
    )
    list_filter = (
        'awards__year',
        'publication_date',
        ('author', RelatedFkAutocompleteFilter),
        ('genres', RelatedM2mAutocompleteFilter),
    )

    # not related to filtering, just showing the original Grappelli feature:
    raw_id_fields = (
        'author', 'genres',
    )
    autocomplete_lookup_fields = {
        'fk': ['author'],
        'm2m': ['genres'],
    }
    # end "not related to ..."

    def awards_list(self, obj):
        return str_list_of_objects(obj.awards.all())
    awards_list.short_description = 'awards'

    def genres_list(self, obj):
        return str_list_of_objects(obj.genres.all())
    genres_list.short_description = 'genres'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    pass
