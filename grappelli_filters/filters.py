from django.templatetags.static import static
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class RelatedAutocompleteFilter(admin.FieldListFilter):
    template = 'grappelli_filters/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.parameter_name = u'{0}__id__exact'.format(field_path)

        super(RelatedAutocompleteFilter, self).__init__(field, request, params, model, model_admin, field_path)
        content_type = ContentType.objects.get_for_model(getattr(model, self.field_path).field.rel.to)
        self.grappelli_trick = u'/{app_label}/{model_name}/t=id'.format(
            app_label=content_type.app_label,
            model_name=content_type.model
        )

    def has_output(self):
        """ Whether to show filter """
        return True

    def choices(self, cl):
        """ Not used, but required by admin_list_filter template tag """
        return ()

    def queryset(self, request, queryset):
        """ Does the actual filtering """
        if self.used_param():
            return queryset.filter(**{self.parameter_name: self.used_param()})

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]

    def used_param(self):
        """ Value from the query string"""
        return self.used_parameters.get(self.parameter_name, '')


class AdminMixin(object):

    class Media:
        js = [static('grappelli_filters/filter.js')]
        css = {
            'all': [static('grappelli_filters/filter.css')],
        }