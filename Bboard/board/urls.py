from django.urls import path
from .views import BulletinListView, BulletinView, AddBulletin


urlpatterns = [
    path('', BulletinListView.as_view(), name='bulletin_list'),
    path('<int:pk>', BulletinView.as_view(), name='bulletin_detail'),
    path('add_bulletin/', AddBulletin.as_view(), name='bulletin_add'),
    # path('search/', NewsSearch.as_view(), name='news_search'),
    # path('addnews/<int:pk>/', UpdateNews.as_view(), name='news_update'),
    # path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    # path('upgrade/', upgrade_me, name='upgrade'),
    # path('<int:pk>/subscribe/', subscribe, name='subscribe'),
]