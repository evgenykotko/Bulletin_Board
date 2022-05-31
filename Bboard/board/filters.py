import django_filters
from django_filters import FilterSet
from .models import Reply


class RepliesFilter(FilterSet):
    text_rep = django_filters.CharFilter(
        field_name='text_rep',
        lookup_expr='icontains',
        label='Текст отзыва'
    )
    bulletin = django_filters.CharFilter(
        field_name='bulletin__title_bul',
        lookup_expr='icontains',
        label='Объявление'
    )

    class Meta:
        model = Reply
        fields = ('bulletin', 'text_rep')
