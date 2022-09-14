import json
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import smtplib
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

@csrf_exempt
def receive(request):
    if request.method == "POST":
        records = json.loads(request.body.decode())
        
        def send_mail(from_addr, to_addr_list, subject, email_body):
            SMTP_SESSION = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            SMTP_SESSION.ehlo()
            SMTP_SESSION.starttls()
            SMTP_SESSION.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            headers = "\r\n".join(["from: " + 'Notification service',
                            "subject: " + subject,
                            "mime-version: 1.0",
                            "content-type: text/html"])

            content = headers + "\r\n\r\n" + email_body
            SMTP_SESSION.sendmail(from_addr, to_addr_list, content)

        for record in records:
            if record['channel'] == 'email':
                email_body = "\r\n".join([record['message'], 
                                    "This notification received on: " + record['created_at'],
                                    "For more information, follow the link: " + record['url']])
                
                send_mail(from_addr = settings.EMAIL_HOST_USER, to_addr_list =[record['email']], subject = record['title'], email_body = email_body)
        


        return redirect("/")


def handle(request):
        subject = "Тема для вашего письма"
        text_content = "Text"
        html_content = get_template('mails/email.html').render()
        from_email = 'django.message1401@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, ['qurol.abdujalilov99@gmail.com'])
        msg.attach_alternative(html_content, "text/html")
        res = msg.send()
        return render(request, "email_app/mail.html")


def sender(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['qurol.abdujalilov99@gmail.com'],
        fail_silently=False,
    )
    return render(request, "email_app/mail.html")