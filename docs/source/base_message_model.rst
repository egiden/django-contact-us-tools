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
        *default: `'enquiries/email.txt' <google.com>`_*

    .. attribute:: HTML_FILE

    .. attribute:: DISP_PRIVACY_POLICY_NOTICE

    .. attribute:: DISP_COPYRIGHT_NOTICE

    .. attribute:: SUBJECT

    .. attribute:: SALUTATION

    .. attribute:: MAIN_CONTENT

    .. attribute:: CLOSING

    .. attribute:: SIGNATURE

``BaseMessage`` methods
-----------------------
.. class:: contact_us_tools.models.BaseMessage

    ``BaseMessage`` has three main methods for controlling the model.

.. function:: BaseMessage.mark_closed(closed_by)

    Marks the matter of the message as resolved. i.e., closed.

    :closed_by: (a django user object) The user that closed the message/ticket

.. autofunction:: contact_us_tools.models.BaseMessage.mark_closed

    

    
