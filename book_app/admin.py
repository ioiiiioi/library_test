from django.contrib import admin
from .models import (
    BookModel,
    LibraryModel
)

# Register your models here.

@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    search_fields = [
        'title'
    ]
    list_display = [
        'title',
        'id',
        'total_copy',
        'available_book'
    ]
    
    @admin.display()
    def available_book(self,obj):
        return obj.available_copy
    
@admin.register(LibraryModel)
class LibraryAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'id',
        'borrowed_by',
        'status',
        'return_at',
    ]
    list_filter = [
        'book',
        'borrowed_by',
        'status'
    ]
