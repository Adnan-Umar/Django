from django.shortcuts import render
from django.core.mail import send_mass_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from django.conf import settings

# Create your views here.
def send_bulk_email(request):
    from_email = settings.DEFAULT_FROM_EMAIL or os.getenv('EMAIL')
    recipient = [from_email]

    message1 = (
        'Welcome User 1',
        'Hello User 1, Welcome to our platform.',
        from_email,
        recipient,
    )

    message2 = (
        'Welcome User 2',
        'Hello User 2, Welcome to our platform.',
        from_email,
        recipient,
    )

    message3 = (
        'Welcome User 3',
        'Hello User 3, Welcome to our platform.',
        from_email,
        recipient,
    )

    send_mass_mail([message1, message2, message3], fail_silently=False)
    return render(request, 'blog/bulk_email.html') 

def send_bulk_email1(request):
    subject = 'Welcome to Our Platform'
    from_email = settings.DEFAULT_FROM_EMAIL or os.getenv('EMAIL')
    recipient_list = [from_email]

    html_content = render_to_string('welcome_email.html', {'username': 'Adnan'})

    msg = EmailMultiAlternatives(subject, "Welcome to My Platform", from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse('Bulk email sent successfully!')