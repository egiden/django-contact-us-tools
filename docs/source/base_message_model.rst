The ``BaseMessage`` model
=========================

About the model
---------------

.. class:: contact_us_tools.models.BaseMessage

    An object representing a user's message which can be either feedback, an enquiry or other.

``BaseMessage`` attributes
--------------------------

.. class:: contact_us_tools.models.BaseMessage

    Asside from the ``BUSINESS_NAME`` and ``COPYRIGHT_YEAR`` attributes discussed in section :doc:`usage`, ``BaseMessage`` offers more attributes to permit further customisation of the automatic-reply email.

    .. attribute:: TICKET_NUM_LEN

        *default: 4*

        The length of the ticket number assigned to the message.
        
    .. attribute:: TEXT_FILE

        *default: "contact_us_tools/email.txt"* `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.txt>`_
        
        The path of the text version of the email template.

    .. attribute:: HTML_FILE

        *default: "contact_us_tools/email.html"* `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.html>`_
        
        The path of the html version of the email template.

    .. attribute:: DISP_PRIVACY_POLICY_NOTICE

        *default: True*
        
        Indicates if privacy policy notice should be included in the email.

    .. attribute:: DISP_COPYRIGHT_NOTICE

        *default: True*
        
        Indicates if copyright notice should be included in the email.

    .. attribute:: SUBJECT

        *default: None*
        
        The email's subject line.

    .. attribute:: SALUTATION

        *default: None*
        
        The email's subject salutation.

    .. attribute:: MAIN_CONTENT

        *default: None*
        
        The email's main content or body. i.e., the content between the salutation and closing.

    .. attribute:: CLOSING

        *default: None*
        
        The email's closing line (without comma).

    .. attribute:: SIGNATURE
        
        *default: None*
        
        The email's signature.

``BaseMessage`` methods
-----------------------
.. class:: contact_us_tools.models.BaseMessage

    ``BaseMessage`` has three main methods for controlling the model.

.. function:: BaseMessage.mark_closed(closed_by)

    Marks the matter of the message as resolved. i.e., closed.

    :closed_by: (a django user object) The user that closed the message/ticket

.. autofunction:: contact_us_tools.models.BaseMessage.mark_closed

    

    
