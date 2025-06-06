Forms
=====

.. py:module:: contact_us_tools.forms

.. class:: BaseContactUsForm

    A subclass of ``django.forms.ModelForm`` that does only two simple things.

    #. Sets the ``Meta`` class's ``fields`` attribute:

        .. code-block:: python

            fields = ['type', 'name', 'email', 'message']

        .. note::

            This form can be used for subclasses of :class:`~contact_us_tools.models.AbstractBaseMessage`, but also :class:`~contact_us_tools.models.AbstractBaseMessageExt` because those are the only fields that concern the user who submitts the form.
    
    #. Adds ``placeholder`` values to the ``name``, ``email``, and ``message`` fields:

        * **name**: "enter your name"

        * **email**: "enter your email address"

        * **message**: "enter your message"