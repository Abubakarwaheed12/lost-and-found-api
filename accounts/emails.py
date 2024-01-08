from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import threading 

def send_email(subject, message, recipient_list, html_template=None, context=None, send_as_html=False):
    from_email = settings.DEFAULT_FROM_EMAIL
    if send_as_html:
        html_template = get_template(html_template)
        html_content = html_template.render(context)
        msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        msg = send_mail(subject, message, from_email, recipient_list)

    
    



def send_threded():
    subject = "Reset Your Password"
    text_content = "This is the text content of the email"
    recipient_list = ["abubakarjutt6346527@gmail.com"]
    thread = threading.Thread(send_email(subject, text_content, recipient_list, send_as_html=True))
    thread.start()
    