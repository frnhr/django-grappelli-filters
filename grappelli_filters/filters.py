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


class SearchFilter(admin.FieldListFilter):
    template = 'admin/filter_search.html'

    def get_parameter_name(self, field_path):
        return u'{0}__icontains'.format(field_path)

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.parameter_name = self.get_parameter_name(field_path)
        super(SearchFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def lookups(self, request, model_admin):
        return ()

    def has_output(self):
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


