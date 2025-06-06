

Usage
=====

How it works
------------

The basic workflow of how a user would use **django-contact-us-tools** is as follows.

#. The user visits the page where the 'contact us' form is rendered.

#. The user enters their name, email and message and submits the form.

#. The app sends an automatic-reply email to the user and redirects to a provided page.

.. _installation:

Installation
------------

To install **django-contact-us-tools**, use pip or an appropriate packaging tool:

.. code-block:: console

   (.venv) $ pip install django-contact-us-tools

Then add ``'contact_us_tools'`` to your :setting:`INSTALLED_APPS` setting:

.. code-block:: python

   INSTALLED_APPS = [
      # ...,
      'contact_us_tools',
   ]

.. _example_setup:

Example Setup
-------------

#. If not using a pre-existing app in your project to handle your website's 'contact us' functionality, create a new app and add it to your :setting:`INSTALLED_APPS` setting:

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

      This step is necessary for the automatic-reply email to be sent.

#. Extend the :py:class:`~contact_us_tools.models.AbstractBaseMessage` model in your app's ``models.py``  and overwrite the :attr:`~contact_us_tools.models.AbstractBaseMessage.BUSINESS_NAME` and :attr:`~contact_us_tools.models.AbstractBaseMessage.COPYRIGHT_YEAR` attributes:
    
   .. code-block:: python

      from contact_us_tools.models import AbstractBaseMessage

      class Message(AbstractBaseMessage):
         BUSINESS_NAME = "My Business Name"
         COPYRIGHT_YEAR = 2025

   :attr:`~contact_us_tools.models.AbstractBaseMessage.BUSINESS_NAME` is your business or website name to be displayed in the :doc:`automatic-reply email <reply_email>` and :attr:`~contact_us_tools.models.AbstractBaseMessage.COPYRIGHT_YEAR` is the year to be displayed with the copyright notice in the email.
   
   .. note::

      Although :py:class:`~contact_us_tools.models.AbstractBaseMessage` is used in the above example, the same process holds true for :py:class:`~contact_us_tools.models.AbstractBaseMessageExt`.

   .. warning::

      :attr:`~contact_us_tools.models.AbstractBaseMessage.BUSINESS_NAME` must be set or else a :py:exc:`ValueError` will be raised. It is the same with :attr:`~contact_us_tools.models.AbstractBaseMessage.COPYRIGHT_YEAR` for the default configuration of :py:class:`~contact_us_tools.models.AbstractBaseMessage`.
   
   .. note::

      If you do not wish to display a copyright notice, and for further customisation options, see the :doc:`models <models>` section.

#. Register the new model to the admin site in your app's ``admin.py``:

    .. code-block:: python
    
            from django.contrib import admin
            from .models import Message

            admin.site.register(Message)

#. Create a new form or extend :py:class:`~contact_us_tools.forms.BaseContactUsForm` and add the ``model`` attribute to the ``Meta`` class:

   .. code-block:: python

      from contact_us_tools.forms import BaseContactUsForm
      from .models import Message

      class ContactUsForm(BaseContactUsForm):
         class Meta(BaseContactUsForm.Meta):
            model = Message

   .. note::
   
      For an in-depth look at :py:class:`~contact_us_tools.forms.BaseContactUsForm`, see the :doc:`forms` section.

#. Create a template for the 'contact us' form and add it to your app's `templates directory <https://docs.djangoproject.com/en/5.2/intro/tutorial03/#writing-your-first-django-app-part-3>`_. Here's a minimal example:

   .. code-block:: html

      <form action="" method="POST">
         {% csrf_token %}

         <legend>Contact Us</legend>
         <small>Got any questions? Fill out this form to reach out.</small>

         {{ form }}

         <button type="submit">Submit</button>
      </form>

#. Use the :py:class:`~contact_us_tools.views.BaseContactUsView` view and create a `URL pattern <https://docs.djangoproject.com/en/5.1/topics/http/urls/#url-dispatcher>`_ to handle the rendering of the form and add it to your project's ``urls.py``, making sure to supply the form, template's name and a 'success url':

   .. code-block:: python

      from django.urls import path
      from contact_us_tools.views import BaseContactUsView
      from .forms import ContactUsForm

      urlpatterns = [
         # ...,
         path('contact-us/', 
               BaseContactUsView.as_view(
                  form_class=ContactUsForm,
                  template_name='template_name',
                  success_url='success_url'),
               name='contact-us'
      )]

   Alternatively, supply the name of the 'success url' using the ``django.urls.reverse`` function:

   .. code-block:: python

      # ...
      from django.urls import reverse

      class ContactUsView(BaseContactUsView):
         form_class = ContactUsForm
         template_name = 'template_name'
         
         def get_success_url(self):
            return reverse('success_url_name')

      urlpatterns = [
         # ...,
         path('contact-us', ContactUsView.as_view(), name='contact-us'),
      ]
         
   .. note::
      
      For an in-depth look at :py:class:`~contact_us_tools.views.BaseContactUsView`, see the :doc:`views` section.

#. Create the models:

   .. code-block:: console

      (.venv) $ python manage.py makemigrations
      (.venv) $ python manage.py migrate

#. Start the development server and visit the relevant url to test the 'contact us' form.

   .. code-block:: console

      (.venv) $ python manage.py runserver

#. Visit the admin site to view the resulting addition to the relevant database table.