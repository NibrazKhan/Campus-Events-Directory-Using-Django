# Campus-Events-Directory-Using-Django
Simple Campus Events Directory Built using Django and Bootstrap as Front-End.
# Author
- Student Name: Nibraz Khan
- Course: Web Application Frameworks

## Overview

The **Campus Events Portal** is a Django-based web application that allows users to submit campus events and browse approved events.  
Event submissions are **moderated by administrators** before becoming publicly visible.

The application demonstrates:

- Django models and database relationships
- Admin-based moderation workflow
- Public event submission
- Secure object retrieval
- Template inheritance with Bootstrap frontend
- CSRF protection
- Custom error pages (404 and 500)

# Features

### Public Users
Users can:

- View **approved events**
- View **event details**
- Browse **event categories**
- View **events within a category**
- Submit **new events for approval**

Submitted events remain **pending until approved by an administrator**.

---

### Administrators
Administrators can:

- Manage event **categories**
- Review submitted **events**
- Approve or reject events through the **Django admin panel**

---

# Technologies Used

- Python 3
- Django 6
- SQLite (default Django database)
- Bootstrap 5
- HTML5
- Django Template Language

# Creater Virtual Environment for the project using:
- python -m venv venv
- Activate the Environment
# Windows
- venv\Scripts\activate
# MacOS/Linux
- source venv/bin/activate
# Install Dependencies
- Install Django using : pip install django
# Database Setup 
- Apply migrations and run the following  commands to create the database tables.
- python manage.py makemigrations
- python manage.py migrate
- This will create the SQLite database (db.sqlite3) and apply the migrations for the project.
# Create Superuser
-  Use the following command: python manage.py createsuperuser
- Enter: Username, Email and Password
- This account will be used to: Manage categories, Review and approve events
# Run the Development Server
- Start the Django development server: python manage.py runserver
- Open the browser and go to : http://127.0.0.1:8000/
# Application URLs
- "/" : View all approved events
- "/events/create": Submit a new event
- "/events/<event_id>" : View event details
- "/categories/" : View all categories
- "/categories/<id>/events : View events for a category
- "/admin/" : Admin moderation dashboard
# Admin Workflow:
- Login to the admin panel using: http://127.0.0.1:8000/admin/
- Create event categories
- Review submitted events
- Mark events as approved
- Once approved, event become visible to public users.
# Security Measures Implemented
- The application includes fundamental security protections:
# CSRF Protection
- {% csrf_token %}
# Safe Object Retrieval
- Event details are retrieved using:
- get_object_or_404()
- This prevents unauthorized access to unapproved events.
# Custom Error Pages.
- Custom error pages are implemented: 404.html – Page not found, 500.html – Internal server error
- These pages prevent sensitive debug information from being displayed.
# Testing Custom Error Pages:
- Custom error pages only appear when:
- DEBUG = False
- To test locally, update in settings.py:
- DEBUG = False, ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
- Then restart the server.
# Bootstrap Frontend
The user interface uses Bootstrap 5 for:
- Responsive layout
- Navigation bar
- Cards for event display
- Styled forms
- Alerts and messages
# Event Submission Flow
- User submits event via Submit Event page
- Event is stored with:
- is_approved = False
- Admin reviews submission
- Admin approves event
- Event becomes visible on the public site
# Notes For Assessors
- This project demonstrates:
- Django MVC architecture
- Admin-based moderation workflow
- Database relationships using ForeignKey
- Form submission with validation
- Template inheritance
- Secure object retrieval
- Custom error handling
