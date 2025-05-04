The ``BaseMessage`` model
=========================

About the model
---------------

.. class:: contact_us_tools.models.BaseMessage

    An object representing a user's message which can be either feedback, an enquiry or other.

``BaseMessage`` variables
-------------------------

TICKET_NUM_LENGTH = 4
    TEXT_FILE = "enquiries/email.txt"
    HMTL_FILE = "enquiries/email.html"
    BUSINESS_NAME = None
    COPYRIGHT_YEAR = None

    SUBJECT = None
    SALUTATION = None,
    MAIN_CONTENT = None,
    CLOSING = None,
    SIGNATURE = None,

    DISP_PRIVACY_POLICY_NOTICE = True
    DISP_COPYRIGHT_NOTICE = True

.. class:: contact_us_tools.models.BaseMessage

    .. attribute:: TICKET_NUM_LEN = "mokm"

        The length of the ticket number assigned to the message.
        Default value: 4

    .. attribute:: TEXT_FILE

    .. attribute:: HTML_FILE

    .. attribute:: DISP_PRIVACY_POLICY_NOTICE

    .. attribute:: DISP_COPYRIGHT_NOTICE

    .. attribute:: COPYRIGHT_YEAR

    .. attribute:: BUSINESS_NAME

    .. attribute:: SUBJECT

    .. attribute:: SALUTATION

    .. attribute:: MAIN_CONTENT

    .. attribute:: CLOSING

    .. attribute:: SIGNATURE
    
