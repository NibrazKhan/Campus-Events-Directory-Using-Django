from django.urls import path
from . import views
# name is used in path for reverse url look up and for easy maintainance
urlpatterns = [
    path("",views.event_list, name = "event_list"),
    path("events/",views.event_list, name = "events"),
    path("events/create/",views.event_create,name="event_create"),
    path("events/<int:event_id>/",views.event_detail,name="event_detail"),
    path("categories/",views.category_list,name="category_list"),
    path("categories/<int:category_id>/events/",views.category_events,name="category_events"),
]