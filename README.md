django-grappelli-filters
====================================

Autocomplete filter for Grappelli

Filter for Foreign key and ManyToMany relations with AJAX autocomplete. Reuses features from Grappelli, works nicely along other filters and with both standard and sidebar filter template...

![Screenshot](docs_img/screenshot.png)

## Usage

Put `grappelli-filters` in your `PYTHONPATH`.

Add `'grappelli-filters'` to `INSTALLED_APPS`

Configure Grappelli autocomplete feature as described [here](https://django-grappelli.readthedocs.org/en/latest/customization.html#autocomplete-lookups). Both Model method and `SETTINGS` value will work fine. For the inpatient, here is the `SETTINGS` value:

    GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
        "myapp": {
            "mycategory": ("id__iexact", "name__icontains",),
        }
    }


In `admin.py` add:

    from grappelli_filters import RelatedAutocompleteFilter, FiltersMixin
 
    class MyModelAdmin(FiltersMixin, admin.ModelAdmin):
        list_filter = ( ... ('field_name', RelatedAutocompleteFilter), ... )
        
        
That's it!
