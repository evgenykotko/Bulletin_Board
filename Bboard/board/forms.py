from django.forms import ModelForm
from .models import Bulletin, Reply
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class AddBulletinForm(ModelForm):
    class Meta:
        model = Bulletin
        fields = ['title_bul', 'body_bul', 'guild_bul']
        widgets = {
            'body_bul': SummernoteWidget(),
        }

class AddReplyBulletinForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['text_rep']

class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

