from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import News
from django.contrib.auth.models import User


@receiver(post_save, sender=News)
def mailing_news(sender, instance, created, **kwargs):
    mail = []
    emails = User.objects.all().values('email')
    for email in emails:
        mail.append(email['email'])
    if created:
        send_mail(
            subject=f'Новостная рассылка от {instance.date_news.strftime("%d %m %Y")}',
            message=f'{instance.title_news}\n{instance.body_news}',
            from_email='bulletin.board.test@yandex.ru',
            recipient_list=mail
        )