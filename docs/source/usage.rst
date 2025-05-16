.. module:: contact_us_tools.models

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

Alternatively, download the `PyPI <https://pypi.org/>`_ source distribution from
`here <https://pypi.python.org/pypi/django-contact-us-tools>`_, decompress the file and run
``python setup.py install`` in the unpacked directory.

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

#. Extend either the :py:class:`~AbstractBaseMessage` or :py:class:`~AbstractBaseMessageExt` model in your app's ``models.py``  and overwrite the :py:attr:`models.AbstractBaseMessage.BUSINESS_NAME` and ``COPYRIGHT_YEAR`` attributes. :attr:`~AbstractBaseMessage.BUSINESS_NAME` is your business or website name to be displayed in the :doc:`automatic-reply email <reply_email>` and ``COPYRIGHT_YEAR`` is the year to be displayed with the copyright notice in the email. :py:class:`~AbstractBaseMessage` will be used as an example, but the same process holds for :py:class:`~AbstractBaseMessageExt`:
    
   .. code-block:: python

      from contact_us_tools.models import AbstractBaseMessage

      class Message(AbstractBaseMessage):
         BUSINESS_NAME = "My Business Name"
         COPYRIGHT_YEAR = 2025
   
   .. warning::

      ``BUSINESS_NAME`` must be set or else a :py:exc:`ValueError` will be raised. It is the same with ``COPYRIGHT_YEAR`` for the default configuration of :py:class:`~AbstractBaseMessage`.
   
   .. note::

      If you do not wish to display a copyright notice, and for further customisation options, see the :doc:`models <models>` section.

#. Register the new model to the admin site in your app's ``admin.py``:

    .. code-block:: python
    
            from django.contrib import admin
            from .models import Message

            admin.site.register(Message)

#. Create a new form or extend :py:class:`~BaseContactUsForm` and add the ``model`` attribute to the ``Meta`` class. Add the form to your app's ``forms.py`` or where desired:

   .. code-block:: python

      from contact_us_tools.forms import BaseContactUsForm
      from .models import Message

      class ContactUsForm(BaseContactUsForm):
         class Meta(BaseContactUsForm.Meta):
            model = Message

   .. note::
   
      For an in-depth look at ``BaseContactUsForm``, see the :doc:`forms` section.

#. Create a template for the 'contact us' form and add it to your app's `templates directory <https://docs.djangoproject.com/en/5.2/intro/tutorial03/#writing-your-first-django-app-part-3>`_. Here's a minimal example:

   .. code-block:: html

      <form action="" method="POST">
         {% csrf_token %}

         <legend>Contact Us</legend>
         <small>Got any questions? Fill out this form to reach out.</small>

         {{ form }}

         <button type="submit">Submit</button>
      </form>

#. Use the ``BaseContactUsView`` view and create a `URL pattern <https://docs.djangoproject.com/en/5.1/topics/http/urls/#url-dispatcher>`_ to handle the rendering of the form and add it to your project's ``urls.py``, making sure to supply the form, template's name and a 'success url':

   .. code-block:: python

      from django.urls import path
      from contact_us_tools.view import BaseContactUsView
      from .forms import ContactUsForm

      urlpatterns = [
         # ...,
         path('contact-us', BaseContactUsView.as_view(form_class=ContactUsForm, template_name='template_name', success_url='success_url')),
      ]

   Alternatively, supply the name of the 'success url' using the ``django.urls.reverse`` function:

   .. code-block:: python

      # ...
      from django.urls import reverse

      urlpatterns = [
         # ...,
         path('contact-us', BaseContactUsView.as_view(form_class=ContactUsForm, template_name='template_name', success_url=reverse('success_url_name'))),
      ]
         
   .. note::
      
      For an in-depth look at ``BaseContactUsView``, see the :doc:`views` section.

#. Create the models:

   .. code-block:: console

      (.venv) $ python manage.py makemigrations
      (.venv) $ python manage.py migrate

#. Start the development server and visit the relevant url to test the 'contact us' form.

   .. code-block:: console

      (.venv) $ python manage.py runserver

#. Visit the admin site to view the resulting addition to the relevant database table.