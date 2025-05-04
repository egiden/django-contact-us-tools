from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
import warnings

class BaseMessage(models.Model):
    """Represents a user's message."""
    TICKET_NUM_LENGTH = 4
    TEXT_FILE = "contact_us_tools/email.txt"
    HMTL_FILE = "contact_us_tools/email.html"
    BUSINESS_NAME = None
    COPYRIGHT_YEAR = None

    SUBJECT = None
    SALUTATION = None,
    MAIN_CONTENT = None,
    CLOSING = None,
    SIGNATURE = None,

    DISP_PRIVACY_POLICY_NOTICE = True
    DISP_COPYRIGHT_NOTICE = True
    
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
            more_context=None,
            from_email=None,
            business_name=None,
            copyright_year=None,
            disp_cpr_notice=None,
            disp_pp_notice=None,
            subject=None,
            salutation=None,
            main_content=None,
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

            more_context (dict or None): Dictionary of more items to add to the context to be used when rendering
                the email template. If None, do nothing.

            from_email (string or None): Sender's email address. If None, try using EMAIL_HOST_USER setting.

            business_name (string or None): Name of your business or website to be displayed on the email.
                If None, use BUSINESS_NAME class attribute.

            copyright_year (string or None): Year to be displayed in email's copyright notice.
                If None, use COPYRIGHT_YEAR class attribute.

            disp_cpr_notice (bool or None): Indicates if copyright notice should be displayed on the email.
                Notice is of the form: "<copyright symbol><copyright_year>, <business_name>" if html_file is used.
                                   Or: "copyright <copyright_year>, <business_name>" if text_file is used.
                If None, use DISP_COPYRIGHT_NOTICE class attribute.

            disp_pp_notice (bool or None): Indicates if a privacy policy notice should be displayed in email.
                Notice is of the form: "This email has been sent in accordance with the <business_name> Privacy Policy".
                If None, use DISP_PRIVACY_POLICY_NOTICE class attribute.

            subject (string or None): Email's subject line. If None, use SUBJECT class attribute. But if SUBJECT is None, set
                to string of the form: "Enquiry #<self.ticket_number>".

            salutation (string or None): Email's salutation or greeting. If None, use SALUTATION class attribute. But if
                SALUTATION is None, set to string of the form: "Dear <self.name>".

            main_content (string or None): Email's main content or body. i.e., the content between the salutation and closing.
                If None and MAIN_CONTENT class attribute is also None, do nothing. Content in text_file or html_file will be used.
                Otherwise, use MAIN_CONTENT.

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

        # Make sure the business_name variable is properly set
        if not business_name:
            business_name = self.BUSINESS_NAME

        # Make sure the copyright_year variable is properly set
        if not copyright_year:
            copyright_year = self.COPYRIGHT_YEAR

        # Make sure the disp_cpr_notice variable is properly set
        if not disp_cpr_notice:
            disp_cpr_notice = self.DISP_COPYRIGHT_NOTICE

        # Make sure the disp_pp_notice variable is properly set
        if not disp_pp_notice:
            disp_pp_notice = self.DISP_PRIVACY_POLICY_NOTICE

        # Make sure the subject variable is properly set
        if not subject:
            if not self.SUBEJCT:
                subject = f"Enquiry #{self.ticket_number}"
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
            'business_name': business_name,
            'copyright_year': copyright_year,
            'disp_pp_notice': disp_pp_notice,
            'disp_cpr_notice': disp_cpr_notice,
            'is_main_content_provided': False,
            'salutation': salutation,
            'main_content': '',
            'closing': closing,
            'signature': signature,
        }

        # Update context with more_context
        if more_context:
            context.update(more_context)

        # Make sure the main_content variable is properly set and update context where appropriate
        if not main_content:
            if self.MAIN_CONTENT:
                main_content = self.MAIN_CONTENT
                context.update({'is_main_content_provided': True})
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