# signals.py

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Complaint

@receiver(post_save, sender=Complaint)
def send_complaint_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Complaint Submitted'
        message = 'A new complaint has been submitted. Please review it.'
        recipient_list = [settings.DEFAULT_FROM_EMAIL]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
