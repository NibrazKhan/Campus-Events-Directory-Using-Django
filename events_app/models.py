from django.db import models
from datetime import datetime 
from django.utils import timezone
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # blank = True and null = True is making the field as optional in field and database level
    description = models.TextField(blank=True,null= True)

    # Custom model defined so that when object is referenced , it returns an human readable name in database and in admin panel.
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank= True, null=True)
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    # Defined foreign key relation between event and category , on_delete ensures if a category is deleted, all the other events are deleted.
    # related_name ensures reverse relationship from the related model back to the model
    # Used in templates : {% for event in category.events.all %} {{ event.name }} {% endfor %} 
    # If there were no related_name , we would have written "category.event_set.all()"
    # Foreign key relationship ensured, and foreign key by default creates many to one relationship that is each category contains multiple events.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = "events")
    contact_name = models.CharField(max_length=100)
    # EmailField() automatically uses EmailValidator so it ensures email validation
    contact_email = models.EmailField()
    # auto_now_add sets the current time once when created. auto_now: Update to current time when the object is saved.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # This field will remain by default as false , as when user will create the event, it needs to be approved by the admin.
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank= True)

    # Custom model defined so that when object is referenced , it returns an human readable name in database and in admin panel.
    def __str__(self):
        return self.title
    # Checking end_datetime is later than start_datetime.
    def clean(self):
        # First check if the start_datetime and end_datetime exists so that it does not get failed.
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValidationError({
                    "End Date and Time must be later than the Start Date and Time"
            })
    # Setting approved at automatically when admin approves event
    # Overriding the default save method of django
    def save(self, *args, **kwargs):
        # Setting approved_at automatically on approval
        if self.is_approved and self.approved_at is None:
            self.approved_at = timezone.now()

        # clear approved_at if approval is not there
        if not self.is_approved:
            self.approved_at = None
        # Running this will validate models before saving
        # We are calling this as we are overiding save and using custom clean() method.
        self.full_clean()
        # This calls Django’s actual database save operation after all the custom logic is done.
        # Without this the model won't be saved to the database
        super().save(*args,**kwargs)


    