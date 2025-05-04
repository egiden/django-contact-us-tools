from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
import warnings

class BaseEnquiry(models.Model):
    TICKET_NUM_LENGTH = 4
    TEXT_FILE = "enquiries/email.txt"
    HMTL_FILE = "enquiries/email.html"
    BUSINESS_NAME = "Company"
    COPYRIGHT_YEAR = 2025

    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
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

    def send_email(self, text_file=None, html_file=None, from_email=None, business_name=None, copyright_year=None):
        """
        Send an automatic email to the user notifying them that their enquiry has been received.
        
        If text_file is None, use TEXT_FILE class variable
        If html_file is None, use HTML_FILE class variable
        If from_email is None, try using the EMAIL_HOST_USER class variable.
        If business_name is None, use the BUSINESS_NAME class variable.
        If copyright_year is None, use the COPYRIGHT_YEAR class variable.
        """
        if not from_email:
            try:
                from_email = settings.EMAIL_HOST_USER
            except:
                raise ValueError("Set the EMAIL_HOST_USER setting or input a value for from_email.")
        
        if not text_file:
            text_file = self.TEXT_FILE
        
        if not html_file:
            html_file = self.HMTL_FILE

        if not business_name:
            business_name = self.BUSINESS_NAME

        if not copyright_year:
            copyright_year = self.COPYRIGHT_YEAR
            
        context = {
            'ticket_number': self.ticket_number,
            'name': self.name,
            'message': self.message,
            'date_created': self.date_created,
            'from_email': from_email,
            'business_name': business_name,
            'copyright_year': copyright_year,
        }

        text_content = render_to_string(text_file, context)
        html_content = render_to_string(html_file, context)
        
        msg = mail.EmailMultiAlternatives(
            subject=f"Enquiry #{self.ticket_number}",
            body=text_content,
            from_email=from_email,
            to=[self.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
    class Meta:
        verbose_name_plural = "Enquiries"