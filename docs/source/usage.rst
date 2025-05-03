Usage
=====

.. _installation:

Installation
------------

To install contact-us-tools, use pip or an appropriate packaging tool:

.. code-block:: console

   (.venv) $ pip install django-contact-us-tools

Then add "contact_us_tools" to your ``INSTALLED_APPS`` setting:

.. code-block:: python

   INSTALLED_APPS = [
      # ...,
      "contact_us_tools",
   ]

Quick start
-----------

#. If not using a pre-existing app in your project to handle your website's 'contact us' functionality, create a new app and add it to your ``INSTALLED_APPS`` setting:

   .. code-block:: console

      (.venv) $ python manage.py startapp contact_us

   .. code-block:: python

      INSTALLED_APPS = [
         # ...,
         'contact_us.apps.ContactUsConfig',
      ]

#. Set up the necessary settings for sending emails as detailed in the `django docs <https://docs.djangoproject.com/en/5.2/topics/email/#email-backends>`_. For example, if gmail is your chosen host:

   .. code-block:: python

      EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      EMAIL_HOST = 'smtp.gmail.com'
      EMAIL_USE_TLS = True
      EMAIL_PORT = 587
      EMAIL_HOST_USER = "example@gmail.com"
      EMAIL_HOST_PASSWORD = "exmample"

   .. note::

      This step is necessary for the automatic-reply email to be sent when the user submits the 'contact us' form.

#. Create a `proxy model <https://docs.djangoproject.com/en/5.2/topics/db/models/#proxy-models>`_ in your app's ``models.py`` for the ``BaseEnquiry`` model and override the ``BUSINESS_NAME`` variable:
    
   .. code-block:: python

      from contact_us_tools.models import BaseEnquiry

      class Enquiry(BaseEnquiry):
         BUSINESS_NAME = "My Business Name"

         class Meta:
            proxy = True
   
   .. note::

      * This step is important as ``BUSINESS_NAME``` is the name that will be used to introduce yourself or your business in the automatic-reply email when the user submits the 'contact us' form.

      * The ``BaseEnquiry`` model can be customised further as detailed in the section :doc:`base_enquiry_model`.

#. Register the proxy model to the admin site in your app's ``admin.py``:

    .. code-block:: python
    
            from django.contrib import admin
            from .models import Enquiry

            admin.site.register(Enquiry)

#. Create a template for the 'contact us' form and add it to your app's `templates directory <https://docs.djangoproject.com/en/5.2/intro/tutorial03/#writing-your-first-django-app-part-3>`_:

   .. code-block:: html

      <form action="" method="POST">
         {% csrf_token %}

         <legend>Contact Us</legend>
         <small>Got any questions? Fill out this form to reach out.</small>

         {{ form }}

         <button type="submit">Submit</button>
      </form>

#. Add the ``BaseContactUsView`` view to your project's ``urls.py`` making sure to supply the template's name:

   .. code-block:: python

      from django.urls import path
      from contact_us_tools.view import BaseContactUsView

      urlpatterns = [
         # ...,
         path('contact-us', BaseContactUsView.as_view(template_name='template_name')),
      ]
      
   .. note::
      
      The ``BaseContactUsView`` utilises the ``BaseContactUsForm`` form, the details of which are available in the section :doc:`base_contactus_form`.

#. Create the models:

   .. code-block:: console

      (.venv) $ python manage.py makemigrations
      (.venv) $ python manage.py migrate

#. Start the development server and visit the relevant url to test the 'contact us' form.

   .. code-block:: console

      (.venv) $ python manage.py runserver

#. Visit the admin site to view the resulting addition to the relevant database table.