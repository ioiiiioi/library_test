from django_filters import (
    FilterSet, 
    CharFilter, 
    ChoiceFilter, 
    DateFilter,
)
from .models import LibraryModel
from django.db import models

class BookFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')

class HistoryFilter(FilterSet):
    borrowed_by = CharFilter(method='borrowed_by_filter')
    title = CharFilter(field_name='book__title', lookup_expr='icontains')
    status = ChoiceFilter(field_name='status', choices=LibraryModel.BookStatusEnum.choices)
    borrowed_at = DateFilter(field_name='created_at')
    return_at = DateFilter(field_name='return_at')

    def borrowed_by_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(email__icontains=value) |
            models.Q(username__icontains=value) |
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value) 
        )

