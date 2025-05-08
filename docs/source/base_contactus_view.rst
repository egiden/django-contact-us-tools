The ``BaseContactUsView`` view
==============================

.. module:: contact_us_tools.views

Attributes
----------

.. class:: BaseContactUsView

   .. attribute:: send_email_kwargs
      :type: dict
      :value: {}

      Keyword arguments to pass into the :attr:`BaseMessage.send_email` method.

   .. attribute:: success_message
      :type: str
      :value: 'Your form has been successfully submitted. We will be in contact with you as soon as we can.'

      Message to display upon successful submission of form.

   .. attribute:: include_success_msg
      :type: bool
      :value: True

      Indicates if success message should be displayed.

Methods
-------

.. function:: BaseContactUsView.send_email(form)

   Send automatic-reply email to user.

   :param form: The form.
   :type form: BaseContactUsForm

