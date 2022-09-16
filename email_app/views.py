import json
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


def index(request):
    return render(request, 'email_app/index.html')


@csrf_exempt
def receive(request):
    if request.method == "POST":
        records = json.loads(request.body.decode())

        def handle(data):
            subject = "Тема для вашего письма"
            html_content = render_to_string('mails/email.html', data)
            from_email = 'django.message1401@gmail.com'
            msg = EmailMultiAlternatives(subject, from_email, ['qurol.abdujalilov99@gmail.com'])
            msg.attach_alternative(html_content, "text/html")
            res = msg.send()

        for record in records:
            if record['channel'] == 'email':
                data = {'message': record['message'],
                        'created_at': record['created_at'],
                        'url': record['url']
                        }

                handle(data)

        return redirect("/")


def sender(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['qurol.abdujalilov99@gmail.com'],
        fail_silently=False,
    )
    return render(request, "email_app/mail.html")