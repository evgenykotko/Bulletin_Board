from django.urls import path
from .views import BulletinListView, BulletinView, AddBulletin, UpdateBulletin, DeleteBulletin, SearchReplies,\
    DeleteReply, confirm_rep, up_to_author


urlpatterns = [
    path('', BulletinListView.as_view(), name='bulletin_list'),
    path('<int:pk>', BulletinView.as_view(), name='bulletin_detail'),
    path('add_bulletin/', AddBulletin.as_view(), name='bulletin_add'),
    path('add_bulletin/<int:pk>/', UpdateBulletin.as_view(), name='bulletin_update'),
    path('delete/<int:pk>', DeleteBulletin.as_view(), name='bulletin_delete'),
    path('replies/', SearchReplies.as_view(), name='replies_search'),
    path('replies/<int:pk>', DeleteReply.as_view(), name='replies_delete'),
    path('replies/<int:pk>/confirmation/', confirm_rep, name='confirm'),
    path('up_to_author/', up_to_author, name='up_to_author'),
    # path('search/', NewsSearch.as_view(), name='news_search'),
    # path('addnews/<int:pk>/', UpdateNews.as_view(), name='news_update'),
    # path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    # path('up_to_author/', up_to_author, name='up_to_author'),
    # path('<int:pk>/subscribe/', subscribe, name='subscribe'),
]