# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Genre(models.Model):
    name = models.CharField(
        max_length=250, null=False, blank=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )


@python_2_unicode_compatible
class Award(models.Model):
    name = models.CharField(
        max_length=250, null=False, blank=False)
    year = models.PositiveSmallIntegerField(
        null=False, blank=False)

    class Meta:
        ordering = ('-year', 'name', )

    def __str__(self):
        return '{} {}'.format(self.name, self.year)

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )


@python_2_unicode_compatible
class Language(models.Model):
    name = models.CharField(
        max_length=250, null=False, blank=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )



@python_2_unicode_compatible
class Author(models.Model):
    first_name = models.CharField(
        max_length=250, null=False, blank=True, default='')
    last_name = models.CharField(
        max_length=250, null=False, blank=False)
    first_language = models.ForeignKey(
        to=Language, related_name='authors',
        null=False, blank=False)

    class Meta:
        ordering = ('last_name', 'first_name', )

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return self.first_name or self.last_name

    @staticmethod
    def autocomplete_search_fields():
        return ("last_name__icontains", "first_name__icontains", )


@python_2_unicode_compatible
class Book(models.Model):
    title = models.CharField(
        max_length=250, null=False, blank=False)
    author = models.ForeignKey(
        to=Author, related_name='books',
        null=False, blank=False)
    language = models.ForeignKey(
        to=Language, related_name='books',
        null=False, blank=False)
    publication_date = models.DateTimeField(
        null=True, blank=True)
    genres = models.ManyToManyField(
        to=Genre, related_name='books',
        null=True, blank=True)
    awards = models.ManyToManyField(
        to=Award, related_name='books',
        null=True, blank=True)

    class Meta:
        ordering = ('title', 'author', )

    def __str__(self):
        return '{}, by {}'.format(self.title, self.author)
