The ``BaseMessage`` model
=========================

.. module:: contact_us_tools.models

.. _base_message_attr:

``BaseMessage`` attributes
--------------------------

.. class:: BaseMessage

    Asside from the :py:attr:`BUSINESS_NAME` and :py:attr:`COPYRIGHT_YEAR` attributes discussed in section :doc:`usage`, :py:class:`~BaseMessage` offers more attributes to permit further customisation of the automatic-reply email. With the exception of :py:attr:`BUSINESS_NAME`, a lot of these attributes can be left as is. If customisation is desired however, they can either be changed here directly, or passed as inputs into :py:meth:`BaseMessage.send_email`. It is recommended that they be changed directly.

    .. attention::

        With the exception of :py:attr:`TICKET_NUM_LEN`,  all the following attributes have corressponding input arguments for the :py:meth:`BaseMessage.send_email` method. I if any of said arguments are given a value either than their default of :py:obj:`None` when calling :py:attr:`BaseMessage.send_email`, they will take precedence over their corressponding :py:class:`~BaseMessage` attribute. Consider, for example, the following case.

        .. code-block:: python
            
            class Message(BaseMessage):
                CLOSING = "Yours sincerely"
                COPYRIGHT_YEAR = 2025

                class Meta:
                    proxy = True

            Message.send_email(closing="Thank you")

        The email would feature a closing line that says "Thank you" rather than "Yours sincerely" because the input in the :py:meth:`BaseMessage.send_email` method takes precendence over the corressponding :py:attr:`CLOSING` attribute. **Note:** In practice, the above code would not work as a view would have to be set up first.*

    .. attribute:: TICKET_NUM_LEN

        *default:* 4

        The length of the ticket number assigned to the message.
        
    .. attribute:: TEXT_FILE

        *default:* "contact_us_tools/email.txt" `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.txt>`_
        
        The path of the text version of the email template.

    .. attribute:: HTML_FILE

        *default:* "contact_us_tools/email.html" `source <https://github.com/egiden/django-contact-us-tools/blob/main/contact_us_tools/templates/contact_us_tools/email.html>`_
        
        The path of the html version of the email template.

    .. attribute:: BUSINESS_NAME

        *default:* :py:obj:`None`
        
        The business or website name to be displayed on the email.

    .. attribute:: COPYRIGHT_YEAR

        *default:* :py:obj:`None`
        
        The year displayed on the email's copyright notice.

    .. attribute:: SUBJECT

        *default:* :py:obj:`None`
        
        The email's subject line.

    .. attribute:: SALUTATION

        *default:* :py:obj:`None`
        
        The email's subject salutation.

    .. attribute:: MAIN_CONTENT

        *default:* :py:obj:`None`
        
        The email's main content or body. i.e., the content between the salutation and closing.

    .. attribute:: MAIN_CONTENT_FBK

        *default:* "Thank you very much for your feedback. It is much appreciated."
        
        The email's main content or body for the case when a user submits feedback.

    .. attribute:: CLOSING

        *default:* :py:obj:`None`
        
        The email's closing line (without comma).

    .. attribute:: SIGNATURE
        
        *default:* :py:obj:`None`
        
        The email's signature.

    .. attribute::  REVIEW_LINK

        *default:* :py:obj:`None`

        Link where user can submit a review.

    .. attribute:: DISP_PRIVACY_POLICY_NOTICE

        *default:* :py:obj:`True`
        
        Indicates if a privacy policy notice should be displayed in the email.

    .. attribute:: DISP_COPYRIGHT_NOTICE

        *default:* :py:obj:`True`
        
        Indicates if copyright notice should be displayed in the email.

    .. attribute:: DISP_REVIEW_LINK

        *default:* :py:obj:`True`
        
        Indicates if :py:attr:`REVIEW_LINK` should be displayed in the email.

    .. tip::

        If you do not require any extra data fields and only wish to override attributes or methods, then it is highly recommended that you create a `proxy <https://docs.djangoproject.com/en/5.2/topics/db/models/#proxy-models>`_ for :py:class:`BaseMessage` as seen in the :doc:`usage <usage>` section.

``BaseMessage`` methods
-----------------------

:py:class:`BaseMessage` has three main methods for controlling the model.

.. function:: BaseMessage.mark_closed(closed_by)

    Marks the matter of the message as resolved. i.e., closed.

    :`closed_by`:  (a django user object) The user that closed the message/ticket.

.. function:: BaseMessage.reopen()

    Reopen's the matter of the message.

.. py:function:: BaseMessage.send_email(text_file=None,html_file=None,extra_context=None,from_email=None,disp_cpr_notice=None,disp_pp_notice=None,disp_review_link=None,copyright_year=None,business_name=None,review_link=None,subject=None,salutation=None,main_content=None,main_content_fbk=None,closing=None,signature=None,)

    Sends automatic-reply email to user supplied email.
    
    With the exception of **extra_context**, each input argument corresponds to an :ref:`attribute<base_message_attr>` of the :py:class:`BaseMessage` class. These particular arguments, however, take precedence over those attributes and will therefore be used if given a value either than the default of :py:obj:`None`.

    :param text_file: Directory of the text version of the email template. If :py:obj:`None`, use :py:attr:`TEXT_FILE`. 
    :type text_file: str or None

    :param html_file: Directory of the html version of the email template. If :py:obj:`None`, use :py:attr:`HTML_FILE`.
    :type html_file: str or None

    :param extra_context: Items to add to the context to be used when rendering the email template.
    :type extra_context: dict or None

    :param form_email: Sender's email address. If :py:obj:`None`, use :setting:`EMAIL_HOST_USER`.
    :type from_email: str or None

    :param disp_cpr_notice: Indicates if copyright notice should be displayed in email. If :py:obj:`None`, use :py:attr:`DISP_COPYRIGHT_NOTICE`.
    :type disp_cpr_notice: bool or None

    :param disp_pp_notice: Indicates if privacy policy notice should be displayed in email. If :py:obj:`None`, use :py:attr:`DISP_PRIVACY_POLICY_NOTICE`.
    :type disp_pp_notice: bool or None

    :param disp_review_link: Indicates if **review_link** should be displayed in email. If :py:obj:`None`, use :py:attr:`DISP_REVIEW_LINK`.
    :type disp_review_link: bool or None

    :param copyright_year: Year to be displayed in email's copyright notice. If :py:obj:`None`, use :py:attr:`COPYRIGHT_YEAR`.
    :type copyright_year: int or None

    :param business_name: Name of business or website to display in email. If :py:obj:`None`, use :py:attr:`BUSINESS_NAME`.
    :type business_name: str or None

    :param review_link: Link where user can submit a review. If :py:obj:`None`, use :py:attr:`REVIEW_LINK`.
    :type review_link: str or None

    :param subject: Email's subject line. If :py:obj:`None`, use :py:attr:`SUBJECT`.
    :type subject: str or None

    :param salutation: Email's salutation or greeting. If :py:obj:`None` and :py:attr:`SALUTATION` is :py:obj:`None`, use "Dear <self.name>". If :py:attr:`SALUTATION` is not :py:obj:`None`, use :py:attr:`SALUTATION`.
    :type salutation: str or None

    :param main_content: Email's main content or body. i.e., the content between the **salutation** and **closing**. If :py:obj:`None`, use :py:attr:`MAIN_CONTENT`.
    :type main_content: str or None

    :param main_content_fbk: Like **main_content**, but only if the message type is FEEDBACK. If :py:obj:`None`, use :py:attr:`MAIN_CONTENT_FBK`.
    :type main_content_fbk: str or None

    :param closing: Email's closing line (without comma). If :py:obj:`None` and :py:attr:`CLOSING` is :py:obj:`None`, use "Kind regards". If :py:attr:`CLOSING` is not :py:obj:`None`, use :py:attr:`CLOSING`
    :type closing: str or None

    :param signature: Email's signature. If :py:obj:`None` and :py:attr:`SIGNATURE` is :py:obj:`None`, use **business_name**. If :py:attr:`SIGNATURE` is not :py:obj:`None`, use :py:attr:`SIGNATURE`.
    :type signature: str or None

    
