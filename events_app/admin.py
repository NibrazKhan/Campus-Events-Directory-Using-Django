from django.contrib import admin
from .models import Category, Event

# Register your models here.
# Not using admin.site.register to have list_display and search_fields
# admin.ModelAdmin inherited to have options like list_display
# list_display: Controls which fields of model are displayed on the change list page.
# search_fields: Adds a search bar and specifies the model fields to be searched.
# list_filter : Enables filters on the right sidebar of the change list page.
# prepopulated_fields: Uses JavaScript to automatically generate values for certain fields
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    # search_fields expects iterable like tuple or list that's why a trailing comma is used to define it as tuple
    search_fields = ("name",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # controls which fields or properties of models are displayed as columns on the change list page, without that , there will be a single column representing the __str__() representation of each object.
    list_display = (
        "title",
        "category",
        "start_datetime",
        "end_datetime",
        "contact_name",
        "contact_email",
        "is_approved",
        "approved_at",
        "created_at"
    )
    # it adds a sidebar to the right side to filter list of model instance based on specific fields.
    list_filter = ("is_approved", "category", "start_datetime", "created_at")
    # It enables case insensitive search of the fields
    search_fields = ("title","description","location","contact_name","contact_email")
    # it makes specific fields(which are in list_display) included to be directly editable. Mainly for admin to approve events. 
    list_editable = ("is_approved",)
    # it makes certain fields non-editable and just viewable
    readonly_fields = ("created_at","approved_at")
    # it adds a navigation bar allowing users to filter results by year , month or day
    date_hierarchy = "start_datetime"
    # it allows admin panel to display objects in the list view sorted by created_at field in descending order. "-" sign indicates list ot view in descending order
    ordering = ("-created_at",)