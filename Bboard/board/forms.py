from django.forms import ModelForm
from .models import Bulletin
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class AddBulletinForm(ModelForm):
    class Meta:
        model = Bulletin
        fields = ['title_bul', 'body_bul', 'guild_bul']
        widgets = {
            'body_bul': SummernoteWidget(),
            # 'body_bul': SummernoteInplaceWidget(),
        }
