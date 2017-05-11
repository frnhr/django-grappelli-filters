from django.contrib import admin
from django.templatetags.static import static


class FiltersMixin( admin.ModelAdmin ):

    class Media:
        js = (static('grappelli_filters/filter.js'),)
        css = {
            'all': (static('grappelli_filters/filter.css'),),
        }
