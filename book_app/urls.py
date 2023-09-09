from django.urls import path, include
from .views import (
    ListAllBooks,
    BorrowedBooksList,
    RenewedBooks,
    BorrowBooks,
    ReturnBook,
)

urlpatterns = [
    path('list/', ListAllBooks.as_view(), name='list-books'),    
    path('history/', BorrowedBooksList.as_view(), name='history-books'),    
    path('renew/', RenewedBooks.as_view(), name='renew-books'),    
    path('borrow/', BorrowBooks.as_view(), name='borrow-books'),    
    path('return/', ReturnBook.as_view(), name='return-books'),    
]
