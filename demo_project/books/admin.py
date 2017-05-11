# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from operator import attrgetter

from django.contrib import admin

from books.models import (
    Book,
    Author,
    Language,
    Genre,
    Award,
)
from grappelli_filters.admin import FiltersMixin
from grappelli_filters.filters import RelatedFkAutocompleteFilter, \
    RelatedM2mAutocompleteFilter, DateTimeStartFilter, DateTimeEndFilter, \
    SearchFilter
from utils import str_list_of_objects


class AwardNameSearchFilter(SearchFilter):
    title = 'Award'


class AuthorFirstLanguageFilter(RelatedFkAutocompleteFilter):
    title = 'Author\'s first language'


@admin.register(Book)
class BookAdmin(FiltersMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = (
        'title',
        'author',
        'language',
        'authors_first_language',
        'publication_date',
        'genres_list',
        'awards_list',
    )
    list_filter = (
        ('author', RelatedFkAutocompleteFilter),
        ('genres', RelatedM2mAutocompleteFilter),
        ('language', RelatedFkAutocompleteFilter),
        ('author__first_language', AuthorFirstLanguageFilter),
        ('publication_date', DateTimeStartFilter),
        ('publication_date', DateTimeEndFilter),
        ('awards__name', AwardNameSearchFilter),
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

    # well, custom list columns (defined below) are also not related to
    # filtering, strictly speaking i.e. they are not needed for the filters to
    # work, but it's hard to see whether filters are working correctly without
    # them, so...

    def awards_list(self, obj):
        return str_list_of_objects(obj.awards.all())
    awards_list.short_description = 'awards'

    def genres_list(self, obj):
        return str_list_of_objects(obj.genres.all())
    genres_list.short_description = 'genres'

    def authors_first_language(self, obj):
        return obj.author.first_language
    authors_first_language.short_description = 'author\'s first lang.'
    authors_first_language.admin_order_field = 'author__first_language__name'


class BookLanguageFilter(RelatedFkAutocompleteFilter):
    title = 'Published book in language'


@admin.register(Author)
class AuthorAdmin(FiltersMixin, admin.ModelAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    list_display = (
        'first_name',
        'last_name',
        'first_language',
        'books',
        'published_in_genres',
        'awards',
    )
    list_filter = (
        ('books__genres', RelatedM2mAutocompleteFilter),
        ('first_language', RelatedFkAutocompleteFilter),
        ('books__language', BookLanguageFilter),
        ('books__awards', RelatedM2mAutocompleteFilter),
    )

    def books(self, obj):
        return str_list_of_objects(obj.books.all(), attrgetter('title'))

    def awards(self, obj):
        return str_list_of_objects(Award.objects.filter(books__author=obj).distinct())

    def published_in_genres(self, obj):
        return str_list_of_objects(Genre.objects.filter(books__author=obj).distinct())
    published_in_genres.short_description = 'Genres'


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    pass
