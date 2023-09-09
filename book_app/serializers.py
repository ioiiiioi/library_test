from rest_framework import serializers
from rest_framework.exceptions import (
    NotAuthenticated,
    PermissionDenied
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404
from user_app.serailizers import BasicUserSerializer
from user_app.models import User
from .models import (
    BookModel,
    LibraryModel
)

class BookListSerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)
    available_at = serializers.DateField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.available_copy <= 0:
            ret['available'] = 0
            borrowed_books = instance.borrowed_books.all().order_by('return_at').values_list('return_at', flat=True)
            ret['available_at'] = borrowed_books[0]
        else:
            ret['available'] = instance.available_copy
            ret['available_at'] = timezone.now()
        return ret 
    
    class Meta:
        model = BookModel
        fields = [
            'id',
            'title',
            'available',
            'available_at',
        ]

class RenewAndHistoryBookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    book_title = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    borrowed_by = BasicUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    return_at = serializers.DateField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['book_title'] = instance.book.title
        return ret
    
    class Meta:
        model = LibraryModel
        fields = [
            'id',
            'book_title',
            'borrowed_by',
            'status',
            'return_at',
            'created_at',
        ]

class BorrowBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(read_only=True)
    return_at = serializers.DateField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['book_title'] = instance.book.title
        ret['borrowed_by'] = BasicUserSerializer(get_object_or_404(User, pk=ret['borrowed_by'])).data
        return ret

    class Meta:
        model = LibraryModel
        fields = [
            'id',
            'book',
            'book_title',
            'borrowed_by',
            'status',
            'created_at',
            'created_by',
            'return_at',
        ]

class ReturnedBookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    status = serializers.CharField(read_only=True)
    book_title = serializers.CharField(read_only=True)
    return_at = serializers.DateField(read_only=True)
    borrowed_by = BasicUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    messages = serializers.CharField(read_only=True)

    def validate_return_time(self, instance):
        msg = None
        if instance.return_at < timezone.now().date():
            msg = _("This book has pass return period.")
        return msg

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['book_title'] = instance.book.title
        ret['messages'] = self.validate_return_time(instance)
        return ret

    class Meta:
        model = LibraryModel
        fields = [
            'id',
            'book_title',
            'borrowed_by',
            'status',
            'created_at',
            'return_at',
            'messages',
        ]