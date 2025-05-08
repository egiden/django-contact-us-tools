from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
import warnings

send_email_arg_names = [
    "text_file",
    "html_file",
    "extra_context",
    "from_email",
    "disp_cpr_notice",
    "disp_pp_notice",
    "disp_review_link",
    "copyright_year",
    "business_name",
    "review_link",
    "subject",
    "salutation",
    "main_content",
    "main_content_fbk",
    "closing",
    "signature",
]

class BaseMessage(models.Model):
    TICKET_NUM_LENGTH = 4
    TEXT_FILE = "contact_us_tools/email.txt"
    HMTL_FILE = "contact_us_tools/email.html"
    BUSINESS_NAME = None
    COPYRIGHT_YEAR = None

    SUBJECT = None
    SALUTATION = None
    MAIN_CONTENT = None
    MAIN_CONTENT_FBK = "Thank you very much for your feedback. It is much appreciated."
    CLOSING = None
    SIGNATURE = None

    REVIEW_LINK = None

    DISP_PRIVACY_POLICY_NOTICE = True
    DISP_COPYRIGHT_NOTICE = True
    DISP_REVIEW_LINK = True
    
    class Type(models.TextChoices):
        ENQUIRY = 'ENQUIRY', 'Enquiry'
        FEEDBACK = 'FEEDBACK', 'Female'
        OTHER = 'OTHER', 'Other/Misc'

    _type = models.CharField("type", max_length=8, choices=Type.choices)
    name=models.CharField(max_length=50, help_text="Name of sender")
    email=models.EmailField(max_length=50, help_text="Email address of sender")
    message=models.TextField()
    date_created = models.DateField(default=timezone.now)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateField(blank=True, null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def ticket_number(self):
        """
        A ticket number which is the model's pk expressed a number whose number of digits is
        specified by TICKET_NUM_LENGTH.
        """
        if not self.pk:
            warnings.warn(f"The {self.__class__.__name__} object with a pk of {self.pk} does not exist.")
            return "".zfill(self.TICKET_NUM_LENGTH)
        return str(self.pk).zfill(self.TICKET_NUM_LENGTH)
    
    def mark_closed(self, closed_by):
        """Close the enquiry."""
        self.is_closed = True
        self.date_closed = timezone.now()
        self.closed_by = closed_by
    
    def reopen(self):
        """Reopen the enquiry."""
        self.is_closed = False
        self.date_closed = None
        self.closed_by = None

    def send_email(self,
            text_file=None,
            html_file=None,
            extra_context=None,
            from_email=None,
            disp_cpr_notice=None,
            disp_pp_notice=None,
            disp_review_link=None,
            copyright_year=None,
            business_name=None,
            review_link=None,
            subject=None,
            salutation=None,
            main_content=None,
            main_content_fbk=None,
            closing=None,
            signature=None,
        ):
        """
        Send an automatic-reply email to the user notifying them that their enquiry has been received.

        Parameters:
            text_file (string or None): Directory of the text version of the email template.
                If None, use TEXT_FILE class attribute.

            html_file (string or None): Directory of the hmtl version of the email template.
                If None, use HTML_FILE class attribute.

            *NOTE: If using custom values for text_file or html_file, the django.template.loader.render_to_string
            function might prove useful.

            extra_context (dict or None): Items to add to the context to be used when rendering
                the email template. If None, do nothing.

            from_email (string or None): Sender's email address. If None, try using EMAIL_HOST_USER setting.

            disp_cpr_notice (bool or None): Indicates if copyright notice should be displayed on the email.
                Notice is of the form: "<copyright symbol><copyright_year>, <business_name>" if html_file is used.
                                   Or: "copyright <copyright_year>, <business_name>" if text_file is used.
                If None, use DISP_COPYRIGHT_NOTICE class attribute.

            disp_pp_notice (bool or None): Indicates if a privacy policy notice should be displayed in email.
                Notice is of the form: "This email has been sent in accordance with the <business_name> Privacy Policy".
                If None, use DISP_PRIVACY_POLICY_NOTICE class attribute.

            disp_review_link (bool or None): Indicates if link to submit a review should be displayed in email.
                Link displayed like so: "We would love to hear your feedback. Please leave us a review at <review_link>."
                If None, use DISP_REVIEW_LINK class attribute.

            copyright_year (int or None): Year to be displayed in email's copyright notice.
                If None, use COPYRIGHT_YEAR class attribute.

            business_name (string or None): Name of business or website to display in the email.
                If None, use BUSINESS_NAME class attribute.

            review_link (str or None): Link where use can submit a review.
                If None, use REVIEW_LINK class attribute.

            subject (string or None): Email's subject line. If None, use SUBJECT class attribute. But if SUBJECT is None, set
                to string of the form: "Message Received #<self.ticket_number>: <self._type>".

            salutation (string or None): Email's salutation or greeting. If None, use SALUTATION class attribute. But if
                SALUTATION is None, set to string of the form: "Dear <self.name>".

            main_content (string or None): Email's main content or body. i.e., the content between the salutation and closing.
                If None and MAIN_CONTENT class attribute is also None, do nothing. Content in text_file or html_file will be used.
                Otherwise, use MAIN_CONTENT.

            main_content_fbk (string or None): Email's main content or body; like main_conent, but only if the message type is FEEDBACK.

            closing (string or None): Email's closing line (without the comma). If None and CLOSING class attribute is None, use "Kind regards".
                Other wise, use CLOSING.

            signature (string or None): Email's signature. If None and SIGNATURE class attribute is None, use business_name. Otherwise, use SIGNATURE.
        """
        # Raise error if the BaseQuery object has not been created and saved
        if not self.pk:
            raise self.DoesNotExist("The {} object does not exist. Save the object to the database first, and then try sending the email.".format(self.__class__.__name__))

        # Make sure the from_email variable is properly set
        if not from_email:
            try:
                from_email = settings.EMAIL_HOST_USER
            except:
                raise ValueError("Set the EMAIL_HOST_USER setting or input a value for from_email.")
            
        # Make sure the text_file variable is properly set
        if not text_file:
            text_file = self.TEXT_FILE
        
        # Make sure the html_file variable is properly set
        if not html_file:
            html_file = self.HMTL_FILE

        # Make sure the disp_cpr_notice variable is properly set
        if not disp_cpr_notice:
            disp_cpr_notice = self.DISP_COPYRIGHT_NOTICE

        # Make sure the disp_pp_notice variable is properly set
        if not disp_pp_notice:
            disp_pp_notice = self.DISP_PRIVACY_POLICY_NOTICE

        # Make sure the disp_review_link variable is properly set
        if not disp_review_link:
            disp_review_link = self.DISP_REVIEW_LINK

        # Make sure the copyright_year variable is properly set
        if not copyright_year:
            copyright_year = self.COPYRIGHT_YEAR

        # Make sure the business_name variable is properly set
        if not business_name:
            business_name = self.BUSINESS_NAME

        # Make sure the review_link variable is properly set
        if not review_link:
            review_link = self.REVIEW_LINK

        # Make sure the subject variable is properly set
        if not subject:
            if not self.SUBEJCT:
                subject = f"Message Received #{self.ticket_number}: {self._type}"
            else:
                subject = self.SUBJECT
        
        # Make sure the salutation variable is properly set
        if not salutation:
            if not self.SALUTATION:
                salutation = f"Dear {self.name}"
            else:
                salutation = self.SALUTATION

        # Make sure the closing variable is properly set
        if not closing:
            if not self.CLOSING:
                closing = "Kind regards"
            else:
                closing = self.CLOSING

        # Make sure the signature variable is properly set
        if not signature:
            if not self.SIGNATURE:
                signature = business_name
            else:
                signature = self.SIGNATURE

        # Initialise the context for rendering the email template
        context = {
            'ticket_number': self.ticket_number,
            'type': self._type,
            'name': self.name,
            'message': self.message,
            'date_created': self.date_created,
            'from_email': from_email,
            'disp_pp_notice': disp_pp_notice,
            'disp_cpr_notice': disp_cpr_notice,
            'disp_review_link': disp_review_link,
            'copyright_year': copyright_year,
            'business_name': business_name,
            'review_link': review_link,
            'is_main_content_provided': False,
            'salutation': salutation,
            'main_content': '',
            'closing': closing,
            'signature': signature,
        }

        # Update context with extra_context
        if extra_context:
            context.update(extra_context)

        # Make sure the main_content variable is properly set and update context where appropriate
        if not main_content_fbk:
            main_content_fbk = self.MAIN_CONTENT_FBK

        if not main_content:
            context.update({'is_main_content_provided': True})
            if not self.MAIN_CONTENT and self._type == self.Type.FEEDBACK:
                main_content = main_content_fbk
            elif self.MAIN_CONTENT:
                main_content = self.MAIN_CONTENT
        else:
            context.update({'is_main_content_provided': True})

        context.update({'main_content': main_content})

        # Create the body text for the email
        text_content = render_to_string(text_file, context)
        html_content = render_to_string(html_file, context)

        # Create and send the email message
        msg = mail.EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[self.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def save(self, *args, **kwargs):
        self._check_business_name()
        self._check_copyright_year()
        return super().save(*args, **kwargs)
    
    def _check_business_name(self):
        """Raise an error if the BUSINESS_NAME variable has not been set."""
        if self.BUSINESS_NAME is None:
            raise ValueError(
                "The BUSINESS_NAME variable for {} has not been set.".format(
                    self.__class__.__name__
                )
            )
    
    def _check_copyright_year(self):
        """Raise an error if the COPYRIGHT_YEAR variable has not been set and DISP_COPYRIGHT_NOTICE is True."""
        if self.COPYRIGHT_YEAR is None and self.DISP_COPYRIGHT_NOTICE == True:
            raise ValueError(
                "The COPYRIGHT_YEAR variable for {} has not been set.".format(
                    self.__class__.__name__
                )
            )
    
    class Meta:
        verbose_name_plural = "Enquiries"