# coding=utf-8
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


class AbstractFieldListFilter(admin.FieldListFilter):
    template = ''
    filter_parameter = None
    url_parameter = None

    def get_parameter_name(self, field_path):
        """ Query parameter name for the URL """
        if self.url_parameter:
            return self.url_parameter
        raise NotImplementedError

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.parameter_name = self.get_parameter_name(field_path)
        title_attr = self.title
        super(AbstractFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.title = title_attr or self.title

    def has_output(self):
        """ Whether to show filter """
        return True

    def lookups(self, request, model_admin):
        """ Not using lookups """
        return ()

    def choices(self, cl):
        """ Not used, but required by admin_list_filter template tag """
        return ()

    def queryset(self, request, queryset):
        """ Does the actual filtering """
        if self.used_param():
            filter_parameter = self.filter_parameter if self.filter_parameter else self.parameter_name
            return queryset.filter(**{filter_parameter: self.used_param()})

    def expected_parameters(self):
        """
        Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]

    def used_param(self):
        """ Parsed value from the query string"""
        return self.used_parameters.get(self.parameter_name, '')

    def input_value(self):
        """ Value for HTML input element """
        return self.used_param()


class RelatedFkAutocompleteFilter(AbstractFieldListFilter):
    template = 'grappelli_filters/related_autocomplete_fk.html'
    model = None
    # TODO define parameter_name = '{}__id__exact'
    # TODO and use this class as base for M2m

    def get_parameter_name(self, field_path):
        if self.url_parameter:
            field_path = self.url_parameter
        return u'{0}__id__exact'.format(field_path)

    def __init__(self, field, request, params, model, model_admin, field_path):

        super(RelatedFkAutocompleteFilter, self).__init__(field, request, params, model, model_admin, field_path)
        if self.model:
            content_type = ContentType.objects.get_for_model(self.model)
        else:
            content_type = ContentType.objects.get_for_model(field.rel.to)
        self.grappelli_trick = u'/{app_label}/{model_name}/'.format(
            app_label=content_type.app_label,
            model_name=content_type.model
        )


class RelatedM2mAutocompleteFilter(AbstractFieldListFilter):
    template = 'grappelli_filters/related_autocomplete_m2m.html'
    model = None

    def get_parameter_name(self, field_path):
        if self.url_parameter:
            field_path = self.url_parameter
        return u'{0}__id__in'.format(field_path)

    def __init__(self, field, request, params, model, model_admin, field_path):

        super(RelatedM2mAutocompleteFilter, self).__init__(field, request, params, model, model_admin, field_path)
        if self.model:
            content_type = ContentType.objects.get_for_model(self.model)
        else:
            content_type = ContentType.objects.get_for_model(field.rel.to)
        self.grappelli_trick = u'/{app_label}/{model_name}/'.format(
            app_label=content_type.app_label,
            model_name=content_type.model
        )

    def input_value(self):
        """ Value for HTML input element """
        return ','.join(self.used_param())


class SearchFilter(AbstractFieldListFilter):
    template = 'grappelli_filters/search.html'

    def get_parameter_name(self, field_path):
        return u'{0}__icontains'.format(field_path)


class SearchFilterC(SearchFilter):
    """ Case-sensitive serach filter """

    def get_parameter_name(self, field_path):
        return u'{0}__contains'.format(field_path)


class DateTimeStartFilter(AbstractFieldListFilter):
    template = 'grappelli_filters/datetime_picker.html'
    range_side = 'start'

    def get_parameter_name(self, field_path):
        return u'{0}__gte'.format(field_path)


class DateTimeEndFilter(DateTimeStartFilter):
    range_side = 'end'

    def get_parameter_name(self, field_path):
        return u'{0}__lte'.format(field_path)