from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user}'

class Guild(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return f'{self.name}'

class Bulletin(models.Model):
    date_bul = models.DateTimeField(auto_now_add=True)
    title_bul = models.TextField()
    body_bul = models.TextField()
    author_bul = models.ForeignKey(Author, on_delete=models.CASCADE)
    guild_bul = models.ManyToManyField(Guild)
    def __str__(self):
        return f'{self.title_bul}'
    def get_absolute_url(self):
        return reverse('bulletin_detail', kwargs={'pk': self.pk})

class Reply(models.Model):
    date_rep = models.DateTimeField(auto_now_add=True)
    text_rep = models.TextField()
    user_rep = models.ForeignKey(User, on_delete=models.CASCADE)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE, related_name='replies')
    confirmation = models.BooleanField(default=False)

    def confirm(self):
        self.confirmation = True
        self.save()

