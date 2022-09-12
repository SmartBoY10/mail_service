import json
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import smtplib
from django.conf import settings

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



