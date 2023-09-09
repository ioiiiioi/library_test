from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from libraryapi.abstract_models import BaseModels
from user_app.models import User
from rest_framework.exceptions import NotFound

# Create your models here.

class BookModel(BaseModels):
    title = models.CharField(max_length=100)
    total_copy = models.IntegerField(default=1)

    @property
    def available_copy(self):
        return self.total_copy - self.borrowed_books.count()

    def __str__(self) -> str:
        return self.title

class LibraryModel(BaseModels):
    
    class BookStatusEnum(models.TextChoices):
        BORROWED = ("BORROWED", "BORROWED")
        RENEWED = ("RENEW", "RENEW")
        RETURNED = ("RETURNED", "RETURNED")

    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='borrowed_books')
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    status = models.CharField(max_length=8, choices=BookStatusEnum.choices)
    return_at = models.DateField(default=timezone.now().date()+timezone.timedelta(days=30))
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.book.available_copy - 1 < 0:
                raise NotFound(detail=_("Books has not been available, wait for someone to return."))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.book.title} - {self.borrowed_by.username}"