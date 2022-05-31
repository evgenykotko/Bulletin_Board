from django.contrib import admin
from .models import Bulletin, Guild, Author, Reply, News
# Register your models here.
admin.site.register(Bulletin)
admin.site.register(Guild)
admin.site.register(Author)
admin.site.register(Reply)
admin.site.register(News)