from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")
        subject = 'Welcome to Adnan'
        message = f'Hi {instance.username}, thank you for registering at Adnan Blog!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
        print("Welcome email sent successfully")