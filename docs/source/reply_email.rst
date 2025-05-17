The automatic-reply email
=========================

The two versions
----------------

There are two versions of the automatic-reply email template. The ``text`` version which is indicated by :attr:`AbstractBaseMessage.TEXT_FILE` and the ``html`` version which is indicated by :attr:`AbstractBaseMessage.HTML_FILE`. This, according to `django <https://docs.djangoproject.com/en/5.2/topics/email/#updating-the-default-content-type>`_, guarantees that any receipient will be able to read the email, irrespective of their mail client. :func:`AbstractBaseMessage.send_email` is able to use both versions by utilising the ``django.core.mail.EmailMultiAlternatives`` class in its implementation.

We will explore both versions, but with the following example scenario.

.. code-block:: python

    class Message(AbstractBaseMessage):
        BUSINESS_NAME = "Stark Industries"
        COPYRIGHT_YEAR = 2025
        SIGNATURE = "Social Media Team"
        DISP_REVIEW_LINK = True
        REVIEW_LINK = "www.starkindustries.com/review"

The text version
----------------
The ``text`` version of the email is of the form:

.. code-block:: text
    :linenos:

    [salutation]

    [main_content]

    [closing],
    [signature]

    -------------------------------------------------
    [name], [date_created]

    Your Message:
    Type: [type]
    [message]
    -------------------------------------------------

    E: [from_email]

    We would love to hear your feedback. Please leave us a review at [review_link].

    This email has been sent in accordance with the [business_name] Privacy Policy

    copyright [copyright_year] [business_name]

An example would then look like.

.. code-block

The html version
----------------