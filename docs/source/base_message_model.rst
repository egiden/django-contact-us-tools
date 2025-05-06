The ``BaseMessage`` model
=========================

About the model
---------------

.. class:: contact_us_tools.models.BaseMessage

    An object representing a user's message which can be either feedback, an enquiry or other.

.. _base_message_attr:

``BaseMessage`` attributes
--------------------------

.. class:: contact_us_tools.models.BaseMessage

    Asside from the ``BUSINESS_NAME`` and ``COPYRIGHT_YEAR`` attributes discussed in section :doc:`usage`, ``BaseMessage`` offers more attributes to permit further customisation of the automatic-reply email. With the exception of ``BUSINESS_NAME``, a lot of these attributes can be left as is. If customisation is desired however, they can either be changed here directly, or passed as inputs into the send_email method. It is recommended that they be changed directly.

    .. warning::

        With the exception of ``TICKET_NUM_LEN``,  all the following attributes have corressponding input arguments for the ``BaseMessage.send_email`` method.

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
        
        Indicates if a privacy policy notice should be included in the email.

    .. attribute:: DISP_COPYRIGHT_NOTICE

        *default: True*
        
        Indicates if copyright notice should be included in the email.

    .. attribute:: COPYRIGHT_YEAR

        *default: None*
        
        The year displayed on the email's copyright notice.

    .. attribute:: BUSINESS_NAME

        *default: None*
        
        The business or website name to be displayed on the email.

    .. attribute:: SUBJECT

        *default: None*
        
        The email's subject line.

    .. attribute:: SALUTATION

        *default: None*
        
        The email's subject salutation.

    .. attribute:: MAIN_CONTENT

        *default: None*
        
        The email's main content or body. i.e., the content between the salutation and closing.

    .. attribute:: MAIN_CONTENT_FBK

        *default: "Thank you very much for your feedback. It is much appreciated."*
        
        The email's main content or body for the case when a user submits feedback.

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

    **closed_by:**  (a django user object) The user that closed the message/ticket

    - closed_by: Aoij sdpo ksd

.. function:: BaseMessage.reopen()

    Reopen's the matter of the message.

.. function:: BaseMessage.send_email(text_file=None,html_file=None,more_context=None,from_email=None,business_name=None,copyright_year=None,disp_cpr_notice=None,disp_pp_notice=None,subject=None,salutation=None,main_content=None,main_content_fbk=None,closing=None,signature=None,)

    Sends the user's message as an email.
    
    With the exception of **more_context**, each input argument corresponds to an :ref:`attribute<base_message_attr>` of the ``BaseMessage`` class. These particular arguments, however, take precedence over those attributes and will therefore be used if given a value either than the default of ``None``. :py:type:`None`.


    

    
