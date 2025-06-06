Models
======

.. module:: contact_us_tools.models

The ``AbstractBaseMessage`` model
---------------------------------

.. class:: AbstractBaseMessage

    An `abstract base class <https://docs.djangoproject.com/en/5.2/topics/db/models/#abstract-base-classes>`_.

Fields
^^^^^^

:class:`AbstractBaseMessage` objects have the following fields.

.. attribute:: AbstractBaseMessage.type
    :type: CharField

    The type of message. It could be either feedback, an enquiry or other/miscilleneous.

.. attribute:: AbstractBaseMessage.name
    :type: CharField

    Name of the sender.

.. attribute:: AbstractBaseMessage.email
    :type: EmailField

    Email of the sender

.. attribute:: AbstractBaseMessage.message
    :type: TextField

    The sender's message.

.. attribute:: AbstractBaseMessage.date_created
    :type: DateTimeField
    :value: timezone.now

    The date the object was created.

Properties
^^^^^^^^^^

.. py:property:: AbstractBaseMessage.ticket_number
    :classmethod:
    :type: str

    The ticket number to be displayed in the automatic-reply email.
    
    By default, each ticket number is the model's primary key expressed as a number whose length is specified by :attr:`~AbstractBaseMessage.TICKET_NUM_LEN`. For example, if the primary key is 3 and :attr:`~AbstractBaseMessage.TICKET_NUM_LEN` is left as its default value of 4, then,
    
        :code:`ticket_number = "0003"`

    If custom ticket_number numbers are desired, see :ref:`custom_ticket_numbers`.

.. _base_message_attr:

Attributes
^^^^^^^^^^

Asside from the :py:attr:`~AbstractBaseMessage.BUSINESS_NAME` and :py:attr:`~AbstractBaseMessage.COPYRIGHT_YEAR` attributes discussed in section :doc:`usage`, :py:class:`~AbstractBaseMessage` offers more attributes to permit further customisation of the automatic-reply email. With the exception of :py:attr:`~AbstractBaseMessage.BUSINESS_NAME`, a lot of these attributes can be left as is. If customisation is desired however, they can either be overwritten directly, or the inputs into the :py:meth:`~AbstractBaseMessage.send_email` method can be overwritten. It is recommended that they be changed directly.

.. attention::

    With the exception of :py:attr:`~AbstractBaseMessage.TICKET_NUM_LEN`,  all the following attributes have corressponding input arguments for :py:meth:`~AbstractBaseMessage.send_email`. If any of said arguments are given a value either than their default of :py:obj:`None` when calling :py:meth:`~AbstractBaseMessage.send_email`, they will take precedence over their corressponding :py:class:`~AbstractBaseMessage` attribute. Consider, for example, the following case.

    .. code-block:: python
        
        class Message(AbstractBaseMessage):
            CLOSING = "Yours sincerely"
            COPYRIGHT_YEAR = 2025

        Message.send_email(closing="Thank you")

    The email would feature a closing line that says "Thank you" rather than "Yours sincerely" because the input passed into :py:meth:`~AbstractBaseMessage.send_email` takes precendence over the value of the corressponding :py:attr:`~AbstractBaseMessage.CLOSING` attribute. **Note:** In practice, the above code would not work as a view would have to be set up first as seen in the :doc:`usage <usage>` section. It is purely for explanatory purposes.

.. attribute:: AbstractBaseMessage.TICKET_NUM_LEN
    :type: int
    :value: 4

    The length of the ticket number assigned to the message.
    
.. attribute:: AbstractBaseMessage.TEXT_FILE
    :type: str
    :value: "contact_us_tools/email.txt"

    `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.txt>`_
    
    The path of the text version of the email template.

.. attribute:: AbstractBaseMessage.HTML_FILE
    :type: str
    :value: "contact_us_tools/email.html"
    
    `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.html>`_
    
    The path of the html version of the email template.

.. attribute:: AbstractBaseMessage.BUSINESS_NAME
    :type: str or None
    :value: None
    
    The business or website name to be displayed in the email.

.. attribute:: AbstractBaseMessage.COPYRIGHT_YEAR
    :type: str or None
    :value: None
    
    The year displayed in the email's copyright notice.

.. attribute:: AbstractBaseMessage.SUBJECT
    :type: str or None
    :value: None
    
    The email's subject line.

.. attribute:: AbstractBaseMessage.SALUTATION
    :type: str or None
    :value: None
    
    The email's salutation.

.. attribute:: AbstractBaseMessage.MAIN_CONTENT
    :type: str or None
    :value: None
    
    The email's main content or body. i.e., the content between the salutation and closing.

.. attribute:: AbstractBaseMessage.MAIN_CONTENT_FBK
    :type: str
    :value: "Thank you very much for your feedback. It is much appreciated."
    
    The email's main content or body for the case when the type of message submitted is feedback.

.. attribute:: AbstractBaseMessage.CLOSING
    :type: str or None
    :value: None
    
    The email's closing line (without the comma).

.. attribute:: AbstractBaseMessage.SIGNATURE
    :type: str or None
    :value: None
    
    The email's signature.

.. attribute:: AbstractBaseMessage.REVIEW_LINK
    :type: str or None
    :value: None

    Link where user can submit a review.

.. attribute:: AbstractBaseMessage.DISP_PRIVACY_POLICY_NOTICE
    :type: bool
    :value: True
    
    Indicates if a privacy policy notice should be displayed in the email.

.. attribute:: AbstractBaseMessage.DISP_COPYRIGHT_NOTICE
    :type: bool
    :value: True
    
    Indicates if a copyright notice should be displayed in the email.

.. attribute:: AbstractBaseMessage.DISP_REVIEW_LINK
    :type: bool
    :value: False
    
    Indicates if :py:attr:`~AbstractBaseMessage.REVIEW_LINK` should be displayed in the email.

Methods
^^^^^^^

:py:class:`AbstractBaseMessage` has two main methods of concern.

.. py:function:: AbstractBaseMessage.get_email_context(disp_cpr_notice=None,disp_pp_notice=None,disp_review_link=None,copyright_year=None,business_name=None,review_link=None,salutation=None,main_content=None,main_content_fbk=None,closing=None,signature=None,)

    Returns the context dictionary to be used by :py:meth:`~AbstractBaseMessage.send_email` when rendering the email template.
    
    Each input argument corresponds to an :ref:`attribute<base_message_attr>` of the :py:class:`AbstractBaseMessage` class. These particular arguments, however, take precedence over those attributes and will therefore be used if given a value either than the default of :py:obj:`None`. If you wish to overwrite any of them, do it by passing them into :py:meth:`~AbstractBaseMessage.send_email`. 

    :param disp_cpr_notice: Indicates if copyright notice should be displayed in email. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.DISP_COPYRIGHT_NOTICE`.
    :type disp_cpr_notice: bool or None

    :param disp_pp_notice: Indicates if privacy policy notice should be displayed in email. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.DISP_PRIVACY_POLICY_NOTICE`.
    :type disp_pp_notice: bool or None

    :param disp_review_link: Indicates if **review_link** should be displayed in email. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.DISP_REVIEW_LINK`.
    :type disp_review_link: bool or None

    :param copyright_year: Year to be displayed in email's copyright notice. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.COPYRIGHT_YEAR`.
    :type copyright_year: int or None

    :param business_name: Name of business or website to display in email. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.BUSINESS_NAME`.
    :type business_name: str or None

    :param review_link: Link where user can submit a review. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.REVIEW_LINK`.
    :type review_link: str or None

    :param salutation: Email's salutation or greeting. If :py:obj:`None` and :py:attr:`~AbstractBaseMessage.SALUTATION` is :py:obj:`None`, use "Dear :py:attr:`~AbstractBaseMessage.name`". If :py:attr:`~AbstractBaseMessage.SALUTATION` is not :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.SALUTATION`.
    :type salutation: str or None

    :param main_content: Email's main content or body. i.e., the content between the **salutation** and **closing**. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.MAIN_CONTENT`.
    :type main_content: str or None

    :param main_content_fbk: Like **main_content**, but only if the message type is FEEDBACK. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.MAIN_CONTENT_FBK`.
    :type main_content_fbk: str or None

    :param closing: Email's closing line (without comma). If :py:obj:`None` and :py:attr:`~AbstractBaseMessage.CLOSING` is :py:obj:`None`, use "Kind regards". If :py:attr:`~AbstractBaseMessage.CLOSING` is not :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.CLOSING`
    :type closing: str or None

    :param signature: Email's signature. If :py:obj:`None` and :py:attr:`~AbstractBaseMessage.SIGNATURE` is :py:obj:`None`, use **business_name**. If :py:attr:`~AbstractBaseMessage.SIGNATURE` is not :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.SIGNATURE`.
    :type signature: str or None

    .. note::

        Overwrite this method if an entirely different context dictionary is required, ensuring to return a ``dict`` object.

        .. code-block:: python
            
            class Message(AbstractBaseMessage):
                BUSINESS_NAME = "My Business Name"
                COPYRIGHT_YEAR = 2025

                def get_email_context(self, **kwargs):
                    return my_context

        However, if you simply want to add to the context, then this will suffice:

        .. code-block:: python

            def get_email_context(self, **kwargs):
                context = super().get_email_context(**kwargs)
                new_items = {} # items you wish to add to the context
                context.update(new_items)
                return context


.. py:function:: AbstractBaseMessage.send_email(text_file=None,html_file=None,from_email=None,subject=None,**kwargs,)

    Sends automatic-reply email to the user's supplied email.
    
    As with :py:meth:`~AbstractBaseMessage.get_email_context`, each input argument corresponds to an :ref:`attribute<base_message_attr>` of the :py:class:`AbstractBaseMessage` class.

    :param text_file: Directory of the text version of the email template. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.TEXT_FILE`. 
    :type text_file: str or None

    :param html_file: Directory of the html version of the email template. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.HTML_FILE`.
    :type html_file: str or None

    :param form_email: Sender's email address. If :py:obj:`None`, use :setting:`EMAIL_HOST_USER`.
    :type from_email: str or None

    :param subject: Email's subject line. If :py:obj:`None`, use :py:attr:`~AbstractBaseMessage.SUBJECT`.
    :type subject: str or None


.. _custom_ticket_numbers:

Custom ticket numbers
^^^^^^^^^^^^^^^^^^^^^

If you desire a custom ticket numbering system, then simply overwrite the :py:obj:`AbstractBaseMessage.ticket_number` property:

.. code-block:: python

    class Message(AbstractBaseMessage):
        
        @property
        def ticket_number(self):
            # my logic
            # return my_ticket_number

More functionality with the ``AbstractBaseMessageExt`` model
------------------------------------------------------------

.. class:: AbstractBaseMessageExt

    An extention of :class:`AbstractBaseMessage` which provides extra fields and methods which allow the messages to be marked as either closed (the matter is resolved) or open. It is itself an `abstract base class <https://docs.djangoproject.com/en/5.2/topics/db/models/#abstract-base-classes>`_ and so will need to be extended if its added functionality desired. See :ref:`extending AbstractBaseMessageExt<extending>`.

The extra fields
^^^^^^^^^^^^^^^^

:class:`AbstractBaseMessageExt` objects have all the fields of :class:`AbstractBaseMessage` with three more.

.. attribute:: AbstractBaseMessageExt.is_closed
    :type: BooleanField
    :value: False

    Indicates if the matter of the message is closed/resolved or open/unresolved.

.. attribute:: AbstractBaseMessage.date_closed
    :type: DateTimeField

    The date the matter was closed.

.. attribute:: AbstractBaseMessage.closed_by
    :type: ForeignKey

    The user that closed the matter

The extra methods
^^^^^^^^^^^^^^^^^

:class:`AbstractBaseMessageExt` objects have all the methods of :class:`AbstractBaseMessage` with two more.

.. function:: AbstractBaseMessageExt.mark_closed(closed_by)

    Marks the matter of the message as resolved. i.e., closed.

    :param closed_by:  The user that closed the message/ticket.
    :type closed_by: a django user object

.. function:: AbstractBaseMessageExt.reopen()

    Reopen's the matter of the message.

.. _extending:

Extending ``AbstractBaseMessage`` and ``AbstractBaseMessageExt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To extent :class:`AbstractBaseMessage` or :class:`AbstractBaseMessageExt`, see :ref:`example_setup` and follow the steps. Concerning forms, views and models alone, your code should be similar to the following if put in one file:

.. code-block:: python

    from contact_us_tools.models import AbstractBaseMessageExt
    from contact_us_tools.forms import BaseContactUsForm
    from contact_us_tools.views import BaseContactUsView

    class AbstractBaseMessage(AbstractBaseMessageExt):
        pass

    class ContactUsForm(BaseContactUsForm):
        class Meta(BaseContactUsForm.Meta):
            model = AbstractBaseMessage

    class ContactUsView(BaseContactUsView):
        form_class = ContactUsForm



