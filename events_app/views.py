from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import Category,Event

def event_create(request):
    categories = Category.objects.all()
    # Dictionary to store the errors
    errors = {}
    # Dictionary to store the forms datas
    form_data = {}
    # As event submission must be POST
    if request.method == "POST":
        form_data = {
            # Retrieves the input, defaults to empty strings if no input given and removes any leading or trailing whitespace.
            "title": request.POST.get("title","").strip(),
            "description": request.POST.get("description","").strip(),
            "location":request.POST.get("location","").strip(),
            "start_datetime": request.POST.get("start_datetime","").strip(),
            "end_datetime": request.POST.get("end_datetime","").strip(),
            "category": request.POST.get("category","").strip(),
            "contact_name": request.POST.get("contact_name","").strip(),
            "contact_email": request.POST.get("contact_email","").strip(),
        }
        title = form_data["title"]
        description = form_data["description"]
        location = form_data["location"]
        start_datetime_str = form_data["start_datetime"]
        end_datetime_str = form_data["end_datetime"]
        category_id = form_data["category"]
        contact_name = form_data["contact_name"]
        contact_email = form_data["contact_email"]

        # Required field validation: Field validation messages if the inputs are not given, stored in error dict
        if not title:
            errors["title"] = "Title is required."
        if not location:
            errors["location"] = "Location is required."
        if not start_datetime_str:
            errors["start_datetime"] = "Start date and time is required."
        if not end_datetime_str:
            errors["end_datetime"] = "End date and time is required."
        if not category_id:
            errors["category"] = "Please select a category."
        if not contact_name:
            errors["contact_name"] = "Contact name is required."
        if not contact_email:
            errors["contact_email"] = "Contact email is required."

        # Parse datetimes
        start_datetime = None
        end_datetime = None

        if start_datetime_str:
            # converting string representation of date to datetime object having a specific dateformat, if the format is wrong an error is given.
            try:
                start_datetime = datetime.strptime(start_datetime_str,"%Y-%m-%dT%H:%M")
            except ValueError:
                errors["start_datetime"]= "Enter a valid start date and time."

        if end_datetime_str:
            try:
                end_datetime = datetime.strptime(end_datetime_str,"%Y-%m-%dT%H:%M")
            except ValueError:
                errors["end_datetime"] = "Enter a valid end date and time."

        # Validate category
        selected_category = None
        if category_id:
            try:
                selected_category = Category.objects.get(id=category_id)
            # If not valid category, either the Category does not exist or the string ID was passed whereas it was expecting integer.
            except (Category.DoesNotExist,ValueError):
                errors["category"] = "Selected category is invalid."

        # Date Order Validation
        # Key Validation
        if start_datetime and end_datetime:
            if end_datetime <= start_datetime:
                errors["end_datetime"] = "End date and time must be later than start date and time."
        
        # Create and validate model if no manual errors so far
        if not errors:
            event = Event(
                title = title,
                description = description,
                location = location,
                start_datetime = start_datetime,
                end_datetime = end_datetime,
                category = selected_category,
                contact_name = contact_name,
                contact_email = contact_email,
                # is_approved stays False by default as it is pending approval still from admin ( Key Requirements )
            )

            try:
                # If the event is successfully created by the user , full_clean() and save() validate the model and write to DB.
                event.full_clean()
                event.save()
                messages.success(
                    request,
                    "Your event has been submitted successfully and is pending approval."
                )
                # Directs user to a URL named "event_create" in urls.py after a view processes data
                return redirect("event_create")
            except ValidationError as e:
                # Extracting the error messages per fields and assigning the first error message in errors dictionary
                for field,message_list in e.message_dict.items():
                    errors[field] = message_list[0]
    # passing this dict to the template.
    context = {
        "categories": categories,
        "errors": errors,
        "form_data": form_data,
    }
    return render(request, "events_app/event_create.html",context)

def event_list(request):
    # For testing internal server error.
    # x=1/0
    # fetching all the event objects which is approved with joining category related to event organized by start_datetime
    events = Event.objects.filter(is_approved=True).select_related("category").order_by("start_datetime")
    return render(request, "events_app/event_list.html",{"events":events})

# details of event based on the event_id
def event_detail(request,event_id):
    # select_related is used to fetch the Event and also to fetch its related Category(JoIN query) in the same database query , thus optimizing it.
    # this ensures invalid event id , unapproved event id, and no direct unsafe retrieval
    event = get_object_or_404(Event.objects.select_related("category"), 
                              id = event_id,
                              is_approved = True )
    return render(request,"events_app/event_detail.html",{"event":event})

# category list by name 

def category_list(request):
    # Displays all categories. Categories are read-only for public users and managed only via Django admin.
    categories = Category.objects.all().order_by("name")
    return render(request,"events_app/category_list.html",{"categories": categories})

# fetching the approved events based on the category
def category_events(request,category_id):
    category = get_object_or_404(Category,id = category_id)
    events = Event.objects.filter(
        category = category,
        is_approved = True
    ).select_related("category").order_by("start_datetime")

    context = {
        "category":category,
        "events" : events,
    }
    return render(request,"events_app/category_events.html",context)

# Custom error views
def custom_404(request, exception):
    return render(request,"errors/404.html",status=404)

def custom_500(request):
    return render(request,"errors/500.html",status=500)
