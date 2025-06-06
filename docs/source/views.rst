Views
=====

.. module:: contact_us_tools.views

.. class:: BaseContactUsView

   A subclass of ``django.views.generic.FormView`` which facilitates the rendering of :py:class:`~contact_us_tools.forms.BaseContactUsForm` and the sending of the automatic-reply email.

Attributes
----------

.. attribute:: BaseContactUsView.send_email_kwargs
   :type: dict
   :value: {}

   Keyword arguments to pass into :meth:`AbstractBaseMessage.send_email()<contact_us_tools.models.AbstractBaseMessage.send_email>` when it is called. See :ref:`sending_email`.

   How it works is, if one were to extend :py:class:`BaseContactUsView` with a non-empty :py:attr:`~BaseContactUsView.send_email_kwargs` attribute like so.

   .. code-block:: python

      class ContactUsView(BaseContactUsView):
         send_email_kwargs = {"closing": "Yours sincerely", "subject": "Message Received!"}

   Then, when :py:class:`BaseContactUsView` calls :meth:`AbstractBaseMessage.send_email()<contact_us_tools.models.AbstractBaseMessage.send_email>`, it would be equivalent to the following.

   .. code-block:: python

      AbstractBaseMessage.send_email(closing="Yours sincerely", subject="Message Received!")

   For further details, see See :ref:`sending_email`.

.. attribute:: BaseContactUsView.success_message
   :type: str
   :value: 'Your form has been successfully submitted. We will be in contact with you as soon as we can.'

   Message to display upon successful submission of form. Override for custom success message

.. attribute:: BaseContactUsView.disp_success_msg
   :type: bool
   :value: True

   Indicates if success message should be displayed.

.. _sending_email:

Sending the automatic-reply email
---------------------------------

.. function:: BaseContactUsView.send_email(form)

   Send automatic-reply email to user by calling :meth:`AbstractBaseMessage.send_email()<contact_us_tools.models.AbstractBaseMessage.send_email>` with input arguments indicated by :py:attr:`~BaseContactUsView.send_email_kwargs`.

   :param form: The form.
   :type form: BaseContactUsForm

   :raises ValueError: If any key in :py:attr:`~BaseContactUsView.send_email_kwargs` is not a valid input into :meth:`AbstractBaseMessage.send_email()<contact_us_tools.models.AbstractBaseMessage.send_email>`.

:py:meth:`BaseContactUsView.send_email` is called when the form used by :py:class:`BaseContactUsView` is validated. For further understanding, consider the following simplified depiction of the source code for :py:class:`BaseContactUsView`.

.. code-block:: python

   class BaseContactUsView:
      
         def send_email(self, form):
            # 1. Check that the keys in the send_email_kwargs attribute are valid.
            # 2. Send the email
            form.instance.send_email(**self.send_email_kwargs)

         def form_valid(self, form):
            self.send_email(form)
            # display success message
            return super().form_valid(form)

.. attention::

   Again, the above is not the actual source code for :py:class:`BaseContactUsView` but an watered-down version of it for comprehension purposes.
