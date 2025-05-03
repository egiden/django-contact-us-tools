=======================
django-contact-us-tools
=======================

A Django app to facilitate 'contact us' functionality.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "contact_us_tools" to your ``INSTALLED_APPS`` setting like so:

    .. code:: python

        INSTALLED_APPS = [
            # ...,
            "contact_us_tools",
        ]

2. Set up the necessary settings for sending emails. For example, if gmail is your chosen host:

    .. code:: python

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_USE_TLS = True
        EMAIL_PORT = 587
        EMAIL_HOST_USER = "example@gmail.com"
        EMAIL_HOST_PASSWORD = "exmample"

    See the django documentation https://docs.djangoproject.com/en/5.2/topics/email/#email-backends

3. Extend the ``BaseEnquiry`` model from the ``contact_us_tools.models`` module and set the ``BUSINESS_NAME`` variable like so:
    
    .. code:: python

        class Enquiry(BaseEnquiry):
            BUSINESS_NAME = "My Business Name"
    
    This is the name that will be used to introduce yourself or your business in the automatic reply email when the user submits the 'contact us' form.

    The ``BaseEnquiry`` model can be configure further. See the docs for details.

4. Register the extended model class ``Enquiry`` from the previous step to the admin site like so:

    .. code:: python
    
            from django.contrib import admin
            admin.site.register(Enquiry)

5. Create a template for the 'contact us' form. For example:

    .. code:: html

        <form action="" method="POST">
            {% csrf_token %}
            {{ form }}

            <button type="submit">Submit</button>
        </form>

6. Add the ``BaseContactUsView`` view from the ``contact_us_tools.views`` module to your project's ``urls.py`` making sure to supply the name of the template for the 'contact us' form like so:

    .. code:: python

        urlpatterns = [
            # ...,
            path('contact-us', BaseContactUsView.as_view(template_name='template_name')),
        ]

    The ``BaseContactUsView`` view can be configure further. See the docs for details.

7. Run ``python manage.py makemigrations`` then ``python manage.py migrate`` to create the models.

8. Start the development server and visit the relevant url to test the 'contact us' form.

9. Visit the admin site to view the resulting addition to the relevant database table.