The automatic-reply email
=========================

.. module:: contact_us_tools.models

The two versions
----------------

There are two versions of the automatic-reply email template. The ``text`` version which is indicated by :attr:`~contact_us_tools.models.AbstractBaseMessage.TEXT_FILE` and the ``html`` version which is indicated by :attr:`~contact_us_tools.models.AbstractBaseMessage.HTML_FILE`. This, according to `django <https://docs.djangoproject.com/en/5.2/topics/email/#updating-the-default-content-type>`_, guarantees that any receipient will be able to read the email, irrespective of their mail client. :meth:`~contact_us_tools.models.AbstractBaseMessage.send_email` is able to use both versions by utilising the ``django.core.mail.EmailMultiAlternatives`` class in its implementation.

We will explore both versions, but with the following example scenario.

.. code-block:: python

    class Message(AbstractBaseMessage):
        BUSINESS_NAME = "Pseudo Industries"
        COPYRIGHT_YEAR = 2025
        SIGNATURE = "Communications Team"
        DISP_REVIEW_LINK = True
        REVIEW_LINK = "www.pseudoindustries.com/review"

The general format
------------------
Each version of the email is of the form:

.. code-block:: text
    :linenos:

    [salutation],

    [main_content]

    [closing],
    [signature]

    -------------------------------------------------
    [name], [date_created]

    Type: [type]

    [message]
    -------------------------------------------------

    E: [from_email]

    We would love to hear your feedback. Please leave us a review at [review_link].

    This email has been sent in accordance with the [business_name] Privacy Policy

    copyright [copyright_year] [business_name]

The text version
----------------

.. code-block:: text
    :linenos:

    Dear Arthur,

    Thank you for contacting us. This is an automated response to confirm that we have received your message.

    Your enquiry has been received and assigned the ticket number #0003. We will review your enquiry and respond as soon as we can. For further questions or assistance, or if you wish to add details or comments to your enquiry, please reply to this email.

    Kind regards,
    Communications Team

    -------------------------------------------------
    Arthur, May 5, 2025, 12:33 a.m

    Type: Enquiry

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sed metus libero. Nullam vehicula eros eu felis vulputate consequat. Vivamus sodales mauris eu consequat finibus. Etiam vel tortor vel metus suscipit luctus sed gravida sem. Duis ac vestibulum lectus. Curabitur eget finibus lacus, eget sollicitudin urna. Sed rutrum sapien vitae ex fermentum, ut tristique purus pharetra. Aliquam imperdiet condimentum dictum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam lobortis neque turpis, in dignissim nibh iaculis quis. Aliquam lacinia pulvinar leo eget egestas.
    -------------------------------------------------

    E: help@pseudoindustries.com

    We would love to hear your feedback. Please leave us a review at www.pseudoindustries.com/review.

    This email has been sent in accordance with the Pseudo Industries Privacy Policy

    copyright 2025 Pseudo Industries

The html version
----------------

.. raw:: html

    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <header>Dear Arthur,</header>
        <main>
            <p>Thank you for contacting us. This is an automated response to confirm that we have received your message.</p>
            <p>
                Your enquiry has been received and assigned the ticket number #0003. We will review your enquiry and respond as soon as we can.
            </p>
            <p>For further questions or assistance, or if you wish to add details or comments to your enquiry, please reply to this email.</p>
            <p>
            Kind regards,
            <br>
            Communications Team
            </p>
        </main>
        <hr>
        <div style="font-style: italic;">
            <p style="font-weight: bold;">Arthur, May 5, 2025, 12:33 a.m</p>
            Type: Enquiry
            <br>
            <br>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sed metus libero. Nullam vehicula eros eu felis vulputate consequat. Vivamus sodales mauris eu consequat finibus. Etiam vel tortor vel metus suscipit luctus sed gravida sem. Duis ac vestibulum lectus. Curabitur eget finibus lacus, eget sollicitudin urna. Sed rutrum sapien vitae ex fermentum, ut tristique purus pharetra. Aliquam imperdiet condimentum dictum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam lobortis neque turpis, in dignissim nibh iaculis quis. Aliquam lacinia pulvinar leo eget egestas.
        </div>
        <hr>
        <footer>
            E: help@pseudoindustries.com
            <br>
            <br>
            We would love to hear your feedback. Please leave us a review at www.pseudoindustries.com/review.
            <br>
            <br>
            This email has been sent in accordance with the Pseudo Industries Privacy Policy
            <br>
            <br>
            &copy2025, Pseudo Industries
        </footer>
    </body>