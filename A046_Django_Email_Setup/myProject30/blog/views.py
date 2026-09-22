from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
import os

# Create your views here.
def send_test_email(request):
    # subject = 'Welcome to My Blog'
    # message = 'Thankyou for subscribing to my Blog.'
    # from_email = 'nouman0537@gmail.com'
    # recipient_list = ['nouman0537@gmail.com']

    # send_mail(subject, message, from_email, recipient_list)  # console backend prints it
    # return HttpResponse('Email sent successfully!')


    # Using EmailMessage for more control
    subject = 'Welcome to My Blog'
    message = render_to_string('email/welcome_email.html', {
        'username': 'Adnan',
        'course': 'Django'
    })
    from_email = settings.DEFAULT_FROM_EMAIL or os.getenv('EMAIL')
    if not from_email or from_email == 'webmaster@localhost':
        raise ImproperlyConfigured(
            "Set the EMAIL environment variable (your Gmail address) before "
            "hitting /send-email/ — e.g. load A046_Django_Email_Setup/.env into "
            "the shell, then restart runserver. Without it, Gmail rejects the send "
            "with SMTPSenderRefused (it saw 'webmaster@localhost')."
        )
    gmail_opts = settings.MAILERS.get('gmail', {}).get('OPTIONS', {})
    if not gmail_opts.get('username') or not gmail_opts.get('password'):
        raise ImproperlyConfigured(
            "Set EMAIL and EMAIL_PASSWORD in the shell (from "
            "A046_Django_Email_Setup/.env) and restart runserver — the 'gmail' "
            "mailer currently has no SMTP credentials, so Gmail would reject "
            "the login."
        )
    email = EmailMessage(
        subject,
        message,
        from_email,  # from_email
        [from_email],  # recipient_list
    )
    email.content_subtype = 'html'  # Main content is now text/html
    email.send(using='gmail')
    return HttpResponse('Email sent successfully through Gmail!')


# To print to the terminal instead of sending, use the console mailer:
#     email.send()                       # uses MAILERS['default'] (console)
# or: send_mail(subject, message, from_email, recipient_list)  # same, console